from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Centralized_Processing.user_login import centralized_processing_user_login
from Handles.handle_login import handle_customer


@require_http_methods(['POST'])
@csrf_exempt
def add_cart(request):
    get_login = centralized_processing_user_login(handle_customer(
        'access_token', token=request.headers.get('Authorization')
    ))
    if not isinstance(get_login, str):
        return get_login
    return JsonResponse({})
