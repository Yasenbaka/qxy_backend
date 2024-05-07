from django.urls import path

from .views import views

from .views.cart import add_cart, delete_cart, get_cart
from .views.order_form import get_order, create_order, delete_order, service_order
from .views.commodity import get_com, add_com

urlpatterns = [
    # 商品
    path('v1/get_com', get_com.get_com),
    path('v1/add_com', add_com.add_com),
    # test api
    path('test', views.test_token_method),

    # api接口
    path('v1/page_main', views.page_main),
    path('v1/exchange_openid', views.exchange_openid),
    path('v1/exchange_token', views.exchange_token),
    path('v1/get_com', views.exchange_token),

    # 购物车
    path('v1/user/add_cart', add_cart.add_cart),
    path('v1/user/delete_cart', delete_cart.delete_cart),
    path('v1/user/get_cart', get_cart.get_cart),

    # 订单
    path('v1/create_order', create_order.create_order),
    path('v1/get_order', get_order.get_order),
    path('v1/delete_order', delete_order.delete_order),
    path('v1/service_order', service_order.change_order_service),

]
