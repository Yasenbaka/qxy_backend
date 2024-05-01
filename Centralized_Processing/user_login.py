from django.http import JsonResponse
from rest_framework import status


def centralized_processing_user_login(execute_handle_login):
    if not execute_handle_login['judge']:
        if 'message' in execute_handle_login:
            return JsonResponse({
                'code': execute_handle_login['code'],
                'error': execute_handle_login['message']
            }, status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({
            'code': execute_handle_login['data'][0],
            'error': execute_handle_login['data'][1]
        }, status=status.HTTP_403_FORBIDDEN)
    return execute_handle_login['openid']
