from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import *

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def products(request):
    products = MedicalAccessories.objects.all()
    return render(request, "products.html", {'products': products})

def appointment(request):
    return render(request, "appointment.html")

def about(request):
    return render(request, "about.html")

def emergency(request):
    return render(request, "emergency.html")

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *

def products(request):
    products = MedicalAccessories.objects.all()
    return render(request, "products.html", {'products': products})

def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_cost = sum(item.quantity * item.accessory.p_cost for item in cart_items)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_cost': total_cost})

def add_to_cart(request, product_id):
    if request.method == 'POST':
        user = request.user  # Assuming you are using Django's built-in authentication
        product = MedicalAccessories.objects.get(pk=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if the item is already in the cart for the user
        cart_item, created = CartItem.objects.get_or_create(user=user, accessory=product)
        
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
        
        return redirect('cart')
    else:
        return redirect('products')

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        user = request.user
        product = MedicalAccessories.objects.get(pk=product_id)
        try:
            cart_item = CartItem.objects.get(user=user, accessory=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
        
    return redirect('cart')
