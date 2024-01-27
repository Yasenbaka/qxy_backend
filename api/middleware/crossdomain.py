from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


class AllowCrossDomain(object):
    def process_request(self, request):
        if request.method == 'OPTIONS':
            response = HttpResponse()
            if 'Access-Control-Request-Method' in request.META.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', ''):
                response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Django, content-type, accept'
            response['Access-Control-Allow-Origin'] = '*'  # 允许任何来源的跨域请求
            return response
        return None