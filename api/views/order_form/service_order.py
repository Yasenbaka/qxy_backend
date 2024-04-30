from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Handles.handle_token import handle_token
from api.models import OrderForm
from wx_users.models import WxUsers


@require_http_methods(['POST'])
@csrf_exempt
def change_order_service(request):
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
    try:
        order_unique_id = int(request.POST['order_unique_id'])
    except KeyError:
        return JsonResponse({
            'code': 10135,
            'error': '缺少必要参数！<order_unique_id>'
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        change_rule = request.POST['change_rule']
    except KeyError:
        return JsonResponse({
            'code': 10135,
            'error': '缺少必要参数！<change_rule>'
        })
    is_order = [None, None]
    if change_rule == 'ongoing_order':
        for item in openid_order.ongoing_order['data']:
            if item['order_unique_id'] == order_unique_id:
                is_order = [True, 'ongoing_order']
                break
            else:
                is_order = False
    elif change_rule == 'closed_order':
        for item in openid_order.closed_order['data']:
            if item['order_unique_id'] == order_unique_id:
                is_order = [True, 'closed_order']
                break
            else:
                is_order = False
    else:
        return JsonResponse({
            'code': 10135,
            'error': '<change_rule>只能接收(ongoing_order),(closed_order)两个参数值！'
        })
    if is_order[0]:
        if is_order[1] == 'ongoing_order':
            openid_order.service_order['data'].append([item for item in openid_order.ongoing_order['data'] if
                                                  item['order_unique_id'] == order_unique_id])
            openid_order.ongoing_order['data'] = [item for item in openid_order.ongoing_order['data'] if
                                                  item['order_unique_id'] != order_unique_id]
        elif is_order[1] == 'closed_order':
            openid_order.service_order['data'].append([item for item in openid_order.closed_order['data'] if
                                                      item['order_unique_id'] == order_unique_id])
            openid_order.closed_order['data'] = [item for item in openid_order.closed_order['data'] if
                                                  item['order_unique_id'] != order_unique_id]
        else:
            return JsonResponse({
                'code': 10135,
                'error': '服务器出现错误！错误点在：change_order_service-1！'
            })
        openid_order.save()
        return JsonResponse({
            'code': 10125,
            'message': f'订单成功删除并登记为售后服务状态！订单号即是售后单号：{order_unique_id}'
        })
    else:
        return JsonResponse({
            'code': 10135,
            'error': f'未在指定的规则<{change_rule}>中找到用户的订单！'
        })