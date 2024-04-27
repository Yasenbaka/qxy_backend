from django.urls import path

from .views import commodity, views, order_form

urlpatterns = [
    path('v1/get_com', commodity.get_com),
    path('v1/add_com', commodity.add_com),
    # test api
    path('test', views.test_token_method),

    # api接口
    path('v1/page_main', views.page_main),
    path('v1/exchange_openid', views.exchange_openid),
    path('v1/exchange_token', views.exchange_token),
    path('v1/get_com', views.exchange_token),

    # 订单
    path('v1/create_order', order_form.create_order),
    path('v1/get_order', order_form.get_order),
    path('v1/delete_order', order_form.delete_order),

]
