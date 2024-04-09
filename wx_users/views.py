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

get_wechat_appid = lambda: settings.WECHAT_APPID
get_wechat_appsecret = lambda: settings.WECHAT_APPSECRET


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
    data = request.POST
    code = data.get('code')
    print('code', code)
    if not code:
        return Response({'code': 400, 'error': 'Code是必要的参数！'}, status=status.HTTP_400_BAD_REQUEST)

        # 使用code向微信服务器请求session_key和openid
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={get_wechat_appid()}&secret={get_wechat_appsecret()}&js_code={code}&grant_type=authorization_code"
    response = requests.get(url)
    wechat_data = response.json()
    openid = wechat_data.get('openid')
    openid = '123'
    print('openid', openid)
    # if not openid:
    #     return Response({'code': 400, 'error': '从微信服务器获取openID失败！客户端问题？'}, status=status.HTTP_400_BAD_REQUEST)

    # user = WxUsers.objects.get(openid=openid)s
    user = WxUsers.objects.get(openid=openid)
    print('user', user)
    refresh = RefreshToken.for_user(user)
    refresh_token = str(refresh)
    print(refresh_token)
    access = RefreshToken(refresh_token).access_token
    print(str(access))
    return JsonResponse({'code': 200, 'message': '登入成功！', 'data': {
        'message': '登入成功！',
        'refreshToken': refresh_token,
        'accessToken': str(access)
    }}, status=status.HTTP_200_OK)
