import json
import random
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from api.handle_token import handle_token
from wx_users.models import WxUsers
from api.models import OrderForm


@require_http_methods(['POST'])
@csrf_exempt
def get_order(request):
    token = request.headers.get('Authorization')
    get_token_re = handle_token(token)
    if not get_token_re['judge']:
        return JsonResponse({
            'code': 10112,
            'error': get_token_re['message']
        }, status=status.HTTP_403_FORBIDDEN)
    openid = get_token_re['openid']
    try:
        WxUsers.objects.get(openid=openid)
    except WxUsers.DoesNotExist:
        return JsonResponse({
            'code': 10117,
            'error': '用户未注册'
        }, status=status.HTTP_403_FORBIDDEN)
    try:
        openid_order = OrderForm.objects.get(openid=openid)
    except OrderForm.DoesNotExist:
        return JsonResponse({
            'code': 10127,
            'message': '用户没有订单！'
        })
    else:
        return JsonResponse({
            'code': 10128,
            'message': '用户全部订单已找到！',
            'data': {
                'ongoing_order': openid_order.ongoing_order,
                'service_order': openid_order.service_order,
                'closed_order': openid_order.closed_order
            }
        })


@require_http_methods(['POST'])
@csrf_exempt
def create_order(request):
    get_token_re = handle_token(request.headers.get('Authorization'))
    if not get_token_re['judge']:
        return JsonResponse({
            'code': 10112,
            'error': get_token_re['message']
        }, status=status.HTTP_403_FORBIDDEN)
    openid = get_token_re['openid']
    try:
        WxUsers.objects.get(openid=openid)
    except WxUsers.DoesNotExist:
        return JsonResponse({
            'code': 10117,
            'error': '用户未注册'
        }, status=status.HTTP_403_FORBIDDEN)
    try:
        OrderForm.objects.get(openid=openid)
    except OrderForm.DoesNotExist:
        order_create = OrderForm.objects.create(openid=openid,
                                                ongoing_order={'data': []},
                                                service_order={'data': []},
                                                closed_order={'data': []})
        order_create.save()
    try:
        openid_order = OrderForm.objects.get(openid=openid)
    except OrderForm.DoesNotExist:
        return JsonResponse({
            'code': 10134,
            'error': '创建订单失败！这是服务器出现问题！'
        }, status=status.HTTP_400_BAD_REQUEST)
    ongoing_order = openid_order.ongoing_order
    try:
        order_details = {
            'order_unique_id': int(time.time()) + random.randint(1, 10000),
            'commodity': int(request.POST['commodity']),
            'count': int(request.POST['count']),
            'price': float(request.POST['price']),
            'coupon': request.POST['coupon']
        }
    except KeyError:
        return JsonResponse({
            'code': 10134,
            'error': '创建订单失败！缺少必要的记录参数！'
        })
    except ValueError:
        return JsonResponse({
            'code': 10134,
            'error': '创建订单失败！传值的参数类型不合法！'
        })
    ongoing_order['data'].append(order_details)
    openid_order.save()
    return JsonResponse({
        'code': 10124,
        'message': '订单创建成功！'
    }, status=status.HTTP_201_CREATED)


@require_http_methods(['POST'])
@csrf_exempt
def delete_order(request):
    get_token_re = handle_token(request.headers.get('Authorization'))
    if not get_token_re['judge']:
        return JsonResponse({
            'code': 10112,
            'error': get_token_re['message']
        }, status=status.HTTP_403_FORBIDDEN)
    openid = get_token_re['openid']
    try:
        WxUsers.objects.get(openid=openid)
    except WxUsers.DoesNotExist:
        return JsonResponse({
            'code': 10117,
            'error': '用户未注册'
        }, status=status.HTTP_403_FORBIDDEN)
    try:
        openid_order = OrderForm.objects.get(openid=openid)
    except OrderForm.DoesNotExist:
        return JsonResponse({
            'code': 10135,
            'error': '用户没有订单！'
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            delete_rule = request.POST['delete_rule']
        except KeyError:
            return JsonResponse({
                'code': 10135,
                'error': '缺少必要参数！<delete_rule>'
            }, status=status.HTTP_400_BAD_REQUEST)
        if delete_rule == 'closed_order':
            try:
                will_delete_order_unique_id = int(request.POST['order_unique_id'])
            except KeyError:
                return JsonResponse({
                    'code': 10135,
                    'error': '缺少必要参数！<order_unique_id>'
                }, status=status.HTTP_400_BAD_REQUEST)
            openid_order.closed_order['data'] = [item for item in openid_order.closed_order['data'] if item['order_unique_id'] != will_delete_order_unique_id]
            openid_order.save()
            return JsonResponse({
                'code': 10125,
                'message': '指定订单删除成功！'
            })

