from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('appointment/', views.appointment, name='appointment'),
    path('emergency/', views.emergency, name='emergency'),
    path('about/', views.about, name='about'),
]


