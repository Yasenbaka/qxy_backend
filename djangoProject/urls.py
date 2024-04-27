"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from api import views as api_views
from api import urls
from wx_users import views as wx_users_views

urlpatterns = [
    path('admin_users/', admin.site.urls),

    # # test api
    # path('api/test', api_views.test_token),
    #
    # # api接口
    # path('api/v1/page_main', api_views.page_main),
    # path('api/v1/exchange_openid', api_views.exchange_openid),
    # path('api/v1/exchange_token', api_views.exchange_token),
    # path('api/v1/get_com', api_views.exchange_token),

    path('api/', include('api.urls')),

    # wx_users微信用户
    path('wx_users/v1/register', wx_users_views.register_user),
    path('wx_users/v1/login', wx_users_views.login_user),
]
