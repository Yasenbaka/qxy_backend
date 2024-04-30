from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Handles.handle_token import handle_token
from api.models import OrderForm
from wx_users.models import WxUsers


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