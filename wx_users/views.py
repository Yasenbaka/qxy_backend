import time

import jwt
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken

from .models import WxUsers
import requests

# 假设你有一个从环境变量或配置文件中获取微信AppID和AppSecret的函数
from django.conf import settings

get_wechat_appid = settings.WECHAT_APPID
get_wechat_appsecret = settings.WECHAT_APPSECRET
get_jwt_alg = settings.SIMPLE_JWT['ALGORITHM']
get_jwt_key = settings.SIMPLE_JWT['SIGNING_KEY']
get_access_token_lifetime = settings.TIME_JWT['ACCESS_TOKEN_LIFETIME']
get_refresh_token_lifetime = settings.TIME_JWT['REFRESH_TOKEN_LIFETIME']


@api_view(['POST'])
@permission_classes((AllowAny,))
def register_user(request):
    data = request.data
    openid = data.get('openid')
    nickname = data.get('nickname')
    avatar_url = data.get('avatarUrl')

    # 这里只是简单的验证，实际应用中应该做更严格的验证
    if not openid:
        return Response({'code': 400, 'error': 'OpenID是必要的参数！'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查用户是否已存在
    try:
        user = WxUsers.objects.get(openid=openid)
        return Response({'code': 200, 'message': '用户已存在！'}, status=status.HTTP_200_OK)
    except WxUsers.DoesNotExist:
        user = WxUsers(openid=openid, nickname=nickname, avatar_url=avatar_url)
        user.save()
        return Response({'code': 201, 'message': '用户注册成功！'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((AllowAny,))
@require_http_methods(["POST"])
def login_user(request):
    code = request.POST.get('code')
    print('code', code)
    if not code:
        return Response({'code': 400, 'error': 'Code是必要的参数！'}, status=status.HTTP_400_BAD_REQUEST)

        # 使用code向微信服务器请求session_key和openid
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={get_wechat_appid}&secret={get_wechat_appsecret}&js_code={code}&grant_type=authorization_code"
    response = requests.get(url)
    wechat_data = response.json()
    openid = wechat_data.get('openid')
    # if not openid:
    #     return Response({'code': 400, 'error': '从微信服务器获取openID失败！客户端问题？'}, status=status.HTTP_400_BAD_REQUEST)
    openid = '123'
    print('openid', openid)
    token_header = {'typ': 'JWT', 'alg': get_jwt_alg}
    token_payload = {'openid': openid, 'exp': int(time.time()) + get_access_token_lifetime}
    access_token = jwt.encode(headers=token_header, payload=token_payload, key=get_jwt_key, algorithm=get_jwt_alg)
    refresh_token = jwt.encode(headers=token_header, payload={
        'access_token': access_token.decode('utf-8'),
        'exp': int(time.time()) + get_refresh_token_lifetime
    }, key=get_jwt_key, algorithm=get_jwt_alg)
    return JsonResponse({
        'code': 200,
        'message': '登入成功！',
        'data': {
            'access_token': access_token.decode('utf-8'),
            'refresh_token': refresh_token.decode('utf-8'),
        }
    })
    # if not openid:
    #     return Response({'code': 400, 'error': '从微信服务器获取openID失败！客户端问题？'}, status=status.HTTP_400_BAD_REQUEST)
    # user = WxUsers.objects.get(openid=openid)
    # user = WxUsers.objects.get(openid=openid)
    # print('user', user)
    # refresh = RefreshToken.for_user(user)
    # refresh_token = str(refresh)
    # access = RefreshToken(refresh_token).access_token
    # access_token = str(access)
    # try:
    #     user_token_library = TokenLibrary.objects.get(openid=openid)
    # except TokenLibrary.DoesNotExist:
    #     user_token_library = TokenLibrary(openid=openid, access_token=access_token, refresh_token=refresh_token, expiration=7, safe_level=5)
    #     user_token_library.save()
    # else:
    #     user_token_library.access_toke, user_token_library.refresh_token = access_token, refresh_token
    #     user_token_library.save()
    # return JsonResponse({'code': 200, 'message': '登入成功！', 'data': {
    #     'message': '登入成功！',
    #     'refreshToken': refresh_token,
    #     'accessToken': str(access)
    # }}, status=status.HTTP_200_OK)
