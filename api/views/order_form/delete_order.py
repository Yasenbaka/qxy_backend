from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Handles.handle_token import handle_token
from api.models import OrderForm
from wx_users.models import WxUsers


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
            will_delete_order_unique_id = int(request.POST['order_unique_id'])
        except KeyError:
            return JsonResponse({
                'code': 10135,
                'error': '缺少必要参数！<order_unique_id>'
            }, status=status.HTTP_400_BAD_REQUEST)
        is_order = None
        for item in openid_order.closed_order['data']:
            if item['order_unique_id'] == will_delete_order_unique_id:
                is_order = True
                break
            else:
                is_order = False
        if is_order:
            openid_order.closed_order['data'] = [item for item in openid_order.closed_order['data'] if
                                                 item['order_unique_id'] != will_delete_order_unique_id]
            openid_order.save()
            return JsonResponse({
                'code': 10125,
                'message': '指定订单删除成功！'
            })
        else:
            return JsonResponse({
                'code': 10135,
                'message': '指定订单删除失败！已结束订单列表中未找到该订单！'
            })