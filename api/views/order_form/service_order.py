from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Centralized_Processing.user_login import centralized_processing_user_login
from Constants.code_status import CodeStatus
from Handles.handle_login import handle_customer
from Handles.handle_token import handle_token
from api.models import OrderForm
from wx_users.models import WxUsers


@require_http_methods(['POST'])
@csrf_exempt
def change_order_service(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    openid = get_login
    user = WxUsers.objects.get(openid=openid)
    try:
        order_type, order_unique_id = request.POST['order_type'], request.POST['order_unique_id']
    except KeyError:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[1]}！缺少必要键值？'
        }, status=status.HTTP_400_BAD_REQUEST)
    if order_type not in ['pending', 'ongoing', 'completed', 'servicing']:
        if order_type == 'pending' or order_type == 'servicing':
            return JsonResponse({
                'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[0],
                'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[1]}！'
                         f'未付款和正在售后服务的订单不能申请售后服务！'
        }, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[1]}！订单类型拼写有误？'
        }, status=status.HTTP_400_BAD_REQUEST)
    if order_unique_id not in user.order[order_type]:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[1]}！'
                     f'在{order_type}订单类型中没有找到该订单号！'
        }, status=status.HTTP_400_BAD_REQUEST)
    if order_unique_id in user.order['servicing']:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_FAILURE[1]}！'
                     f'该订单号正在售后服务中！'
        }, status=status.HTTP_400_BAD_REQUEST)
    user.order['servicing'][order_unique_id] = user.order[order_type][order_unique_id]
    del user.order[order_type][order_unique_id]
    user.save()
    return JsonResponse({
        'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_SUCCESS[0],
        'message': f'售后订单！{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_SUCCESS[1]}'
    })
