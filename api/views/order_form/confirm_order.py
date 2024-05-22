from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Centralized_Processing.user_login import centralized_processing_user_login
from Constants.code_status import CodeStatus
from Handles.handle_login import handle_customer
from wx_users.models import WxUsers


@require_http_methods(['POST'])
@csrf_exempt
def confirm_order(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    openid = get_login
    user = WxUsers.objects.get(openid=openid)
    order_unique_id = request.POST.get('order_unique_id')
    if order_unique_id is None:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_SEARCH_SUCCESS[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_SEARCH_SUCCESS[0]}！缺少必要的键值？'
        })
    if order_unique_id not in user.order['ongoing']:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_SEARCH_SUCCESS[0],
            'error': f'{CodeStatus().BasicCommunication().UserArchive().USER_ORDER_SEARCH_SUCCESS[0]}！'
        })
    user.order['confirmed'][order_unique_id] = user.order['ongoing'][order_unique_id]
    del user.order['ongoing'][order_unique_id]
    user.save()
    return JsonResponse({
        'code': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_SUCCESS[0],
        'message': CodeStatus().BasicCommunication().UserArchive().USER_ORDER_CREATE_SUCCESS[1]
    })
