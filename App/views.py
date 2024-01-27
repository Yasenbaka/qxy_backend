from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
@csrf_exempt
def index(request):
    query_param = request.GET.get('param', None)
    if query_param:
        # 根据 query 参数执行相应的操作
        return Response({"message": "Success", "data": query_param})
    else:
        return Response({"message": "No query param provided"})
