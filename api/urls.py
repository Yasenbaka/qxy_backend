from django.urls import path

from .views import commodity, views

urlpatterns = [
    path('v1/get_com', commodity.get_com),
    # test api
    path('test', views.test_token),

    # api接口
    path('v1/page_main', views.page_main),
    path('v1/exchange_openid', views.exchange_openid),
    path('v1/exchange_token', views.exchange_token),
    path('v1/get_com', views.exchange_token),
]
