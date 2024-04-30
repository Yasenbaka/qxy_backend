from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from api.models import Commodity


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