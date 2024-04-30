from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Handles.handle_token import handle_token

from wx_users.models import WxUsers


@require_http_methods(['POST'])
@csrf_exempt
def add_cart(request):
    token = request.headers.get('Authorization')
    get_token_re = handle_token(token)
    if not get_token_re['judge']:
        return JsonResponse({
            'code': 10112,
            'error': get_token_re['message']
        }, status=status.HTTP_403_FORBIDDEN)
    openid = get_token_re['openid']
    try:
        user = WxUsers.objects.get(openid=openid)
    except WxUsers.DoesNotExist:
        return JsonResponse({
            'code': 10112,
            'error': '用户不存在！'
        })

