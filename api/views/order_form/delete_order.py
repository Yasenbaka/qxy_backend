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
def delete_order(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    openid = get_login
    user = WxUsers.objects.get(openid=openid)
    order_type, order_unique_id = request.POST.get('order_type'), request.POST.get('order_unique_id')
    if order_type is None or order_unique_id is None:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_FAILURE[1]}！缺少必要键值？'
        }, status=status.HTTP_400_BAD_REQUEST)
    if order_type not in ['pending', 'ongoing', 'completed', 'servicing']:
        if order_type == 'ongoing' or order_type == 'servicing':
            return JsonResponse({
                'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_FAILURE[0],
                'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_FAILURE[1]}！'
                         f'正在进行和正在售后服务的订单不能删除！'
        }, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_FAILURE[1]}！订单类型拼写有误？'
        }, status=status.HTTP_400_BAD_REQUEST)
    if order_unique_id not in user.order[order_type]:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_FAILURE[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_FAILURE[1]}！'
                     f'在{order_type}订单类型中没有找到该订单号！'
        }, status=status.HTTP_400_BAD_REQUEST)
    del user.order[order_type][order_unique_id]
    user.save()
    return JsonResponse({
        'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_SUCCESS[0],
        'message': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_DELETE_SUCCESS[1]
    }, status=status.HTTP_200_OK)
