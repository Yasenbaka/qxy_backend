from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Centralized_Processing.user_login import centralized_processing_user_login
from Handles.handle_login import handle_customer

from wx_users.models import WxUsers
from Constants.code_status import CodeStatus

user_archive_status = CodeStatus().BasicCommunication().UserArchive()
fab_status = CodeStatus().BasicCommunication().FaBBasicCommunication()


@require_http_methods(['POST'])
@csrf_exempt
def add_cart(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    openid = get_login
    user = WxUsers.objects.get(openid=openid)
    try:
        (com_unique_id, com_count) = (request.POST.get('com_unique_id'), int(request.POST.get('com_count')))
    except KeyError:
        return JsonResponse({
            'code': fab_status.MISSING_KEY[0],
            'error': fab_status.MISSING_KEY[1]
        }, status=status.HTTP_403_FORBIDDEN)
    except ValueError:
        return JsonResponse({
            'code': fab_status.MISSING_VALUE[0],
            'error': fab_status.MISSING_VALUE[1]
        }, status=status.HTTP_403_FORBIDDEN)
    user.cart[com_unique_id] = {
        'com_unique_id': com_unique_id,
        'com_count': com_count
    }
    user.save()
    return JsonResponse({
        'code': user_archive_status.USER_CART_SUCCESS_ADD[0],
        'message': user_archive_status.USER_CART_SUCCESS_ADD[1]
    }, status=status.HTTP_200_OK)
