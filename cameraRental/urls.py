from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('canoncam/', views.canoncam_view, name='canoncam'),
    path('canonlens/', views.canonlens_view, name='canonlens'),
    path('sonycam/', views.sonycam_view, name='sonycam'),
    path('sonylens/', views.sonylens_view, name='sonylens'),
    path('cart/', views.cart_view, name='cart'),
    path('account/', views.account_view, name='account'),
    path('member/', views.member_view, name='member'),
    path('orders/', views.orders_view, name='orders'),
    path('create_order/', views.create_order, name='create_order'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('check_login_status/', views.check_login_status, name='check_login_status'),
    
    # Add more URL patterns for other views here
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)