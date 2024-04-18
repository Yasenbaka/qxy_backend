import json
import time
from datetime import datetime, timedelta

import jwt
import requests
from django.http import JsonResponse, HttpResponse
from jwt import decode, encode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import MainPageImages
from django.conf import settings

get_wechat_appid = settings.WECHAT_APPID
get_wechat_appsecret = settings.WECHAT_APPSECRET
get_jwt_alg = settings.SIMPLE_JWT['ALGORITHM']
get_jwt_key = settings.SIMPLE_JWT['SIGNING_KEY']
get_access_token_lifetime = settings.TIME_JWT['ACCESS_TOKEN_LIFETIME']
get_refresh_token_lifetime = settings.TIME_JWT['REFRESH_TOKEN_LIFETIME']


def get(request):
    print(request.method)
    if request.method == 'POST' or request.method == 'GET':
        request_dict = request.GET
        print(request_dict)
        name = request_dict['name']
        print(name, type(name))
        return JsonResponse({'message': 'Hello World get!', 'data': request_dict})
    else:
        return JsonResponse({'message': 'type error'})


def get_name(request):
    print(request.method)
    if request.method == 'POST' or request.method == 'GET':
        request_dict = request.GET
        print(request_dict)
        print('get cookie', request.COOKIES.get('login'))
        name = request_dict['name']
        print(name, type(name))
        return JsonResponse({'message': 'Hello World getname!', 'data': request_dict})
    else:
        return JsonResponse({'message': 'type error'})


# code交换openid
def exchange_openid(request):
    request_dict = request.GET
    try:
        code = request_dict.get('code')
    except:
        return JsonResponse({
            'code': 400,
            'error': 'code是必要的参数！',
            'data': {
                'message': 'code是必要的参数！'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        exchange_openid_url = (f"https://api.weixin.qq.com/sns/jscode2session?"
                               f"appid={get_wechat_appid}&"
                               f"secret={get_wechat_appsecret}&"
                               f"js_code={code}&grant_type=authorization_code")
        response = requests.get(exchange_openid_url)
        get_openid = response.json()
        openid = get_openid.get('openid')
        if not openid:
            return JsonResponse({
                'code': 409,
                'error': '对于当前资源状态，请求无法完成!',
                'data': {
                    'message': '对于当前资源状态，请求无法完成！',
                    'openid': openid
                }
            }, status=status.HTTP_409_CONFLICT)
    except:
        return JsonResponse({
            'code': 400,
            'error': '从微信服务器获取openID失败！客户端问题？',
            'data': {
                'message': '从微信服务器获取openID失败！客户端问题？'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({
        'code': 200,
        'data': {
            'message': '成功得到openID！',
            'openid': openid
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def exchange_token(request):
    access_token = request.POST.get('access_token')
    refresh_token = request.POST.get('refresh_token')
    code = request.POST.get('code')
    if not (access_token and refresh_token and code):
        return JsonResponse({
            'code': 403,
            'error': '缺少必要的参数！'
        }, status=status.HTTP_403_FORBIDDEN)
    try:
        decode_refresh_token = jwt.decode(refresh_token, key=get_jwt_key, algorithms=[get_jwt_alg])
    except jwt.exceptions.DecodeError as e:
        # 如果令牌无效或签名不匹配，将会抛出DecodeError异常
        print(f"JWT解码失败: {e}")
        return JsonResponse({
            'code': 403,
            'error': '刷新令牌解码失败！Refresh token decode error!'
        }, status=status.HTTP_403_FORBIDDEN)
    except jwt.exceptions.ExpiredSignatureError:
        # 如果令牌已过期，将会抛出ExpiredSignatureError异常
        print("JWT已过期")
        return JsonResponse({
            'code': 400,
            'error': '刷新令牌过期！Refresh token expired error!'
        }, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.InvalidTokenError:
        # 如果令牌格式不正确或包含无效声明，将会抛出InvalidTokenError异常
        print("有老六传无效的JWT")
        return JsonResponse({
            'code': 400,
            'error': '刷新令牌无效！Refresh token invalid or expired error!'
        }, status=status.HTTP_400_BAD_REQUEST)
    except jwt.PyJWTError:
        print('刷新令牌致命错误！Refresh token important error!')
    else:
        get_refresh_decode_access_token = decode_refresh_token['access_token']
        if get_refresh_decode_access_token != access_token:
            return JsonResponse({
                'code': 400,
                'error': '有老六篡改了请求令牌！Access token check discrepancy!'
            }, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     url = f"https://api.weixin.qq.com/sns/jscode2session?appid={get_wechat_appid}&secret={get_wechat_appsecret}&js_code={code}&grant_type=authorization_code"
        #     response = requests.get(url)
        #     wechat_data = response.json()
        #     openid = wechat_data.get('openid')
        #     if not openid:
        #         return JsonResponse({
        #             'code': 400,
        #             'error': '对于当前资源状态，请求无法完成！'
        #         })
        # except:
        #     return JsonResponse({
        #         'code': 400,
        #         'error': '从微信服务器获取openID失败！客户端问题？'
        #     })
        openid = 123
        token_header = {'typ': 'JWT', 'alg': get_jwt_alg}
        token_payload = {'openid': openid, 'exp': int(time.time()) + get_access_token_lifetime}
        new_access_token = jwt.encode(headers=token_header,
                                      payload=token_payload,
                                      key=get_jwt_key,
                                      algorithm=get_jwt_alg)
        print('新的access_token生成')
        new_refresh_token = jwt.encode(headers=token_header,
                                       payload={
                                           'access_token': new_access_token,
                                           'exp': decode_refresh_token['exp']
                                       }, key=get_jwt_key, algorithm=get_jwt_alg)
        print('新的refresh_token生成')
        return JsonResponse({
            'code': 200,
            'message': '兑换成功！',
            'data': {
                'access_token': new_access_token,
                'refresh_token': new_refresh_token
            }
        })


def test_token(request):
    to_get_access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    return JsonResponse({
        'code': 200,
        'token_lifetime': to_get_access_token_lifetime
    })
    # access_token = request.headers.get('Authorization')
    # print(access_token)
    # try:
    #     # 解码并验证JWT
    #     decoded_token = decode(access_token,
    #                            signing_key=settings.SIMPLE_JWT['SIGNING_KEY'],
    #                            algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
    #     print(decoded_token)
    #     print('decoded_token', decoded_token)
    # except jwt.exceptions.DecodeError as e:
    #     # 如果令牌无效或签名不匹配，将会抛出DecodeError异常
    #     print(f"JWT解码失败: {e}")
    # except jwt.exceptions.ExpiredSignatureError:
    #     # 如果令牌已过期，将会抛出ExpiredSignatureError异常
    #     print("JWT已过期")
    # except jwt.exceptions.InvalidTokenError:
    #     # 如果令牌格式不正确或包含无效声明，将会抛出InvalidTokenError异常
    #     print("有老六传无效的JWT")
    # try:
    #
    #     # 获取令牌的过期时间
    #     exp = decoded_token['exp']
    #     print('exp', exp)
    #
    #     # 将过期时间从Unix时间戳转换为datetime对象
    #     expiration_datetime = datetime.utcfromtimestamp(exp)
    #     print('expiration_datetime', expiration_datetime)
    #
    #     # 获取当前时间并加上一个小的缓冲时间（可选）
    #     now = datetime.utcnow()
    #     print('now', now)
    #
    #     # 检查令牌是否过期
    #     return JsonResponse({'message': expiration_datetime < now})
    # except (jwt.exceptions.DecodeError, KeyError):
    #     # 如果令牌无效或缺少必要的字段，则认为令牌已过期
    #     return JsonResponse({'message': True})


def page_main(request):
    names_to_filter = [
        'mainBanner',
        'mainSecBackgroundImage',
        'iconPopular',
        'iconStationery',
        'iconCreative',
        'iconCustomization',
        'iconLogistics',
        'iconAllProducts',
        'activityBannerFirst',
        'activityBannerSecond',
        'qxyCup',
        'qxyFaceMask',
        'qxyNotebook',
        'qxyPocker',
        'qxyUmbrella',
        'qxyWoodCup',
        'cart',
    ]
    images = MainPageImages.objects.filter(name__in=names_to_filter)
    handle_res_images = {}
    for image in images:
        handle_res_images[image.name] = image.url
    return JsonResponse(handle_res_images, safe=False)
