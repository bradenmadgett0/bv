"""
URL configuration for bluevoice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views

menu_item_list = views.MenuItemsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

menu_item_detail = views.MenuItemsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

cart_list = views.CartViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

cart_detail = views.CartViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create_user'
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve'
})

order_list = views.OrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

order_detail = views.OrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'api/menu', views.MenuItemsViewSet)
router.register(r'api/cart', views.CartViewSet)
router.register(r'api/orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', views.BasicAuthLogin.as_view()),
    path('api/logout/', views.BasicAuthLogin.as_view())
]

urlpatterns += [
    path('api/', include('rest_framework.urls')),
]
