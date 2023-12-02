from django.urls import path

from base.views import home, login_page, register_page, add_cart, cart, remove_cart_items, orders, success, logout_view, \
    check_username_availability

urlpatterns = [
    path('',home,name='home'),
    path('login/',login_page, name='login'),
    path('register/', register_page, name='register'),
    path('cart/', cart, name='cart'),
    path('orders/', orders, name='orders'),
    path('success/', success, name='success'),
    path('logout/', logout_view, name='logout'),



    path('add_cart/<int:id>', add_cart, name='add_cart'),
    path('remove_cart_items/<int:pk>', remove_cart_items, name='remove_cart_items'),
    path('check-check_username_availability/', check_username_availability, name='check_username_availability'),

]