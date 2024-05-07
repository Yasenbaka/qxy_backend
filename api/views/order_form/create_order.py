import time
import hashlib

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Centralized_Processing.user_login import centralized_processing_user_login
from Constants.code_status import CodeStatus
from Handles.handle_login import handle_customer
from wx_users.models import WxUsers


@require_http_methods(['POST'])
@csrf_exempt
def create_order(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    openid = get_login
    user = WxUsers.objects.get(openid=openid)
    order_unique_id = f'{int(time.time() * 1000)}{int(hashlib.sha256(openid.encode()).hexdigest()[:14], 16)}'
    try:
        order_details = {
            'order_unique_id': order_unique_id,
            'commodity': int(request.POST['commodity']),
            'count': int(request.POST['count']),
            'price': float(request.POST['price']),
            'coupon': request.POST['coupon'],
            'create_time': int(time.time()),
        }
    except KeyError:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[1]}！缺少必要的记录参数！'
        })
    except ValueError:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[1]}！传值的参数类型不合法！'
        })
    user.order['pending'][order_unique_id] = order_details
    user.save()
    return JsonResponse({
        'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_SUCCESS[0],
        'message': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_SUCCESS[1]
    }, status=status.HTTP_201_CREATED)
