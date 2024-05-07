from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

import Constants.code_status
from Centralized_Processing.user_login import centralized_processing_user_login
from Handles.handle_login import handle_customer
from wx_users.models import WxUsers

user_archive_status = Constants.code_status.CodeStatus().BasicCommunication().UserArchive()


@require_http_methods(['GET'])
@csrf_exempt
def get_cart(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    openid = get_login
    user = WxUsers.objects.get(openid=openid)
    return JsonResponse({
        'code': user_archive_status.USER_CART_SUCCESS_FOUND[0],
        'message': user_archive_status.USER_CART_SUCCESS_FOUND[1],
        'data': user.cart
    }, status=status.HTTP_200_OK)
