from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('list/', views.goods_list, name='list'),
    path('detail/', views.detail, name='detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('place_order/', views.placeorder, name='place_order'),
    path('site/', views.site, name='site'),
    path('shanchu/', views.shanchu, name='shanchu'),
    path('message/', views.message, name='message'),
    path('create_order/', views.create_order, name='create_order'),
    path('aaa/', views.aaa, name='aaa'),
    path('dell/', views.dell, name='dell'),
    path('order/', views.order, name='order'),
    path('log_off/', views.log_off, name='log_off'),
]