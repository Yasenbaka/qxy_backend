import json

import requests
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response

from api.models import MainPageImages
from django.conf import settings

get_wechat_appid = lambda: settings.WECHAT_APPID
get_wechat_appsecret = lambda: settings.WECHAT_APPSECRET


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
                               f"appid={get_wechat_appid()}&"
                               f"secret={get_wechat_appsecret()}&"
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
