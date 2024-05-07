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
def get_order(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    openid = get_login
    user = WxUsers.objects.get(openid=openid)
    try:
        order_unique_id = request.POST['order_unique_id']
    except KeyError:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().ORD
        })