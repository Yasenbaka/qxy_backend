from django.http import JsonResponse, HttpResponse


def get(request):
    print(request.method)
    if request.method == 'POST' or request.method == 'GET':
        request_dict = request.GET
        print(request_dict)
        name = request_dict['name']
        print(name, type(name))
        return JsonResponse({'message': 'Hello World get!', 'data': request_dict})
    else:
        return JsonResponse({'message': 'type error'})


def get_name(request):
    print(request.method)
    if request.method == 'POST' or request.method == 'GET':
        request_dict = request.GET
        print(request_dict)
        print('get cookie', request.COOKIES.get('login'))
        name = request_dict['name']
        print(name, type(name))
        return JsonResponse({'message': 'Hello World getname!', 'data': request_dict})
    else:
        return JsonResponse({'message': 'type error'})


def my_view(request):
    request_dict = request.GET
    print(request_dict)
    # 设置 cookie
    response = HttpResponse()
    response.set_cookie('login', '123321123321',max_age=7*24*3600, secure=False, httponly=False)
    print(response.cookies)
    # 返回响应
    return response
