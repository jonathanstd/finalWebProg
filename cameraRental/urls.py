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
    
    # Add more URL patterns for other views here
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)