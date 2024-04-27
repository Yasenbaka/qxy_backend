import json
import random
import time

from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from api.models import Commodity
from api.handle_token import handle_token
from admin_users.models import AdminUser


@require_http_methods(['GET'])
@csrf_exempt
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
@csrf_exempt
def add_com(request):
    token = request.headers.get('Authorization')
    get_token_re = handle_token(token)
    if not get_token_re['judge']:
        return JsonResponse({
            'code': 10112,
            'error': get_token_re['message']
        }, status=status.HTTP_403_FORBIDDEN)
    try:
        model_commodity = Commodity()
        model_commodity.unique_id = (int(time.time()) +
                                     len(request.POST['name']) +
                                     len(request.POST['introduce']) +
                                     random.randint(500, 10000))
        (model_commodity.com_name,
         model_commodity.com_introduce,
         model_commodity.com_price,
         model_commodity.com_reserve,
         model_commodity.com_banners,
         model_commodity.com_introduction_pictures,
         model_commodity.com_is_active,
         model_commodity.com_is_preferential,
         model_commodity.com_is_coupon) = (request.POST['name'],
                                           request.POST['introduce'],
                                           request.POST['price'],
                                           request.POST['reserve'],
                                           json.loads(request.POST['banners']),
                                           json.loads(request.POST['introduction_pictures']),
                                           request.POST['is_active'],
                                           request.POST['is_preferential'],
                                           request.POST['is_coupon'])
    except MultiValueDictKeyError:
        return JsonResponse({
            'code': 20110,
            'message': '商品添加失败！缺少必要的参数！'
        }, status=status.HTTP_400_BAD_REQUEST)
    except json.decoder.JSONDecodeError:
        return JsonResponse({
            'code': 20110,
            'message': '商品添加失败！参数中涉及JSON字符串的数据非法！'
        })
    else:
        try:
            AdminUser.objects.get(account=get_token_re['account'])
        except AdminUser.DoesNotExist:
            return JsonResponse({
                'code': 10107,
                'error': '超级管理员未注册！'
            }, status=status.HTTP_403_FORBIDDEN)
        model_commodity.save()
        return JsonResponse({
            'code': 20100,
            'message': '商品添加成功！'
        }, status=status.HTTP_201_CREATED)
