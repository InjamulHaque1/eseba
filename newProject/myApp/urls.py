from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout, name='logout'),
    
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'), 
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'), 
    
    path('appointment/', views.appointment, name='appointment'),
    path('emergency/', views.emergency, name='emergency'),
    path('about/', views.about, name='about')
]
