import jwt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view

from api.models import Commodity
from djangoProject import settings


def get_com(request):
    try:
        unique_id = int(request.GET['unique_id'])
    except KeyError:
        return JsonResponse({'error': '缺少必要参数！<unique_id>'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return JsonResponse({'error': '<unique_id>参数类型错误！'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        model_commodity = Commodity.objects.get(unique_id=unique_id)
        (com_name,
         com_introduce,
         com_price,
         com_reserve,
         com_banners,
         com_introduction_pictures,
         com_is_active,
         com_is_preferential,
         com_is_coupon) = (model_commodity.com_name,
                           model_commodity.com_introduce,
                           model_commodity.com_price,
                           model_commodity.com_reserve,
                           model_commodity.com_banners,
                           model_commodity.com_introduction_pictures,
                           model_commodity.com_is_active,
                           model_commodity.com_is_preferential,
                           model_commodity.com_is_coupon)
        return JsonResponse({
            'code': 200,
            'massage': '请求成功！',
            'data': {
                'unique_id': unique_id,
                'name': com_name,
                'introduce': com_introduce,
                'price': com_price,
                'reserve': com_reserve,
                'banners': com_banners,
                'introduction_pictures': com_introduction_pictures,
                'is_active': com_is_active,
                'is_preferential': com_is_preferential,
                'is_coupon': com_is_coupon
            }
        }, status=status.HTTP_200_OK)
    except Commodity.DoesNotExist:
        return JsonResponse({
            'code': 205,
            'massage': '没有这个商品！',
            'data': {
                'unique_id': unique_id,
            }
        }, status=status.HTTP_205_RESET_CONTENT)


@require_http_methods(['POST'])
def add_com(request):
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({'code': 403, 'error': '未登录请求！'}, status=status.HTTP_403_FORBIDDEN)
    try:
        decode_token = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
    except jwt.exceptions.DecodeError as e:
        # 如果令牌无效或签名不匹配，将会抛出DecodeError异常
        print(f"JWT解码失败: {e}")
        return JsonResponse({
            'code': 403,
            'error': '管理员令牌解码失败！Admin token decode error!'
        }, status=status.HTTP_403_FORBIDDEN)
    except jwt.exceptions.ExpiredSignatureError:
        # 如果令牌已过期，将会抛出ExpiredSignatureError异常
        print("JWT已过期")
        return JsonResponse({
            'code': 400,
            'error': '管理员令牌过期！Admin token expired error!'
        }, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.InvalidTokenError:
        # 如果令牌格式不正确或包含无效声明，将会抛出InvalidTokenError异常
        print("有老六传无效的JWT")
        return JsonResponse({
            'code': 400,
            'error': '管理员令牌无效！Admin token invalid or expired error!'
        }, status=status.HTTP_400_BAD_REQUEST)
    except jwt.PyJWTError:
        print('管理员令牌致命错误！Admin token important error!')
    else:
        token = decode_token.get('admin_token')
        return JsonResponse({})
