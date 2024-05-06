from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

import Constants.code_status
from Centralized_Processing.user_login import centralized_processing_user_login
from Handles.handle_login import handle_customer
from wx_users.models import WxUsers


@require_http_methods(['POST'])
@csrf_exempt
def delete_cart(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    openid = get_login
    user = WxUsers.objects.get(openid=openid)
    try:
        com_unique_id = request.POST.get('com_unique_id')
    except KeyError:
        return JsonResponse({
            'code': Constants.code_status.CodeStatus().BasicCommunication().FaBBasicCommunication().MISSING_KEY[0],
            'error': Constants.code_status.CodeStatus().BasicCommunication().FaBBasicCommunication().MISSING_KEY[1]
        }, status=status.HTTP_403_FORBIDDEN)
    if com_unique_id not in user.cart:
        return JsonResponse({
            'code': Constants.code_status.CodeStatus().BasicCommunication().UserArchive().USER_CART_FAILURE_FOUND[0],
            'error': Constants.code_status.CodeStatus().BasicCommunication().UserArchive().USER_CART_FAILURE_FOUND[1]
        }, status=status.HTTP_403_FORBIDDEN)
    del user.cart[com_unique_id]
    user.save()
    return JsonResponse({
        'code': Constants.code_status.CodeStatus().BasicCommunication().UserArchive().USER_CART_SUCCESS_DELETE[0],
        'message': Constants.code_status.CodeStatus().BasicCommunication().UserArchive.USER_CART_SUCCESS_DELETE[1]
    })
