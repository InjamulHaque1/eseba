from .models import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect

def home(request):
    return render(request, "home.html")

def login(request):
    if request.method == "POST":
        username = request.POST["u_name"]
        password = request.POST["u_password"]
        
        authenticated_user = authenticate(username=username, password=password)
        
        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, f"Welcome, {username}!")
            return render(request, "home.html", {'username' : username})
        
        else:
            messages.error(request, "Try again!")
            return redirect("login")
            
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        u_name = request.POST["u_name"]
        u_email = request.POST["u_email"]
        u_password = request.POST["u_password"]
        u_age = request.POST["u_age"]
        u_address = request.POST["u_address"]
        u_mobile = request.POST["u_mobile"]
        u_gender = request.POST["u_gender"]
        
        # Create a user using Django's built-in authentication
        user = User.objects.create_user(username=u_name, email=u_email, password=u_password)
        user.age = u_age
        user.address = u_address
        user.mobile = u_mobile
        user.gender = u_gender
        user.save()
            
        messages.success(request, "Your account has been successfully created.")
        return redirect("login")
    
    return render(request, "register.html")

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('home')

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
        
        return render(request, "cart.html")
    else:
        return render(request, "products.html")

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        user = request.user
        product = MedicalAccessories.objects.get(pk=product_id)
        try:
            cart_item = CartItem.objects.get(user=user, accessory=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
        
    return render(request, "cart.html")
