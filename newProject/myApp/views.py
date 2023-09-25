from sqlite3 import IntegrityError

from django.urls import reverse
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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

        try:
            # Attempt to create a new user
            user = User.objects.create_user(username=u_name, email=u_email, password=u_password)
            user.age = u_age
            user.address = u_address
            user.mobile = u_mobile
            user.gender = u_gender
            user.save()
            
            authenticated_user = authenticate(username=u_name, password=u_password)
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                messages.success(request, "Your account has been successfully created.")
                return redirect("home")
        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect("register")

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

@login_required
def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    # Calculate the total cost for each item in the cart
    for item in cart_items:
        item.total_cost = item.accessory.p_cost * item.quantity

    # Calculate the total cost for all items in the cart
    total_cost = sum(item.total_cost for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_cost': total_cost})


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(MedicalAccessories, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # Check if the item is already in the cart for the user
        cart_item, created = CartItem.objects.get_or_create(user=user, accessory=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.total_cost = cart_item.quantity * cart_item.accessory.p_cost  # Calculate the total cost
        cart_item.save()

        messages.success(request, "Item added to your cart.")
        return redirect(reverse('cart'))
    else:
        return redirect('products')  # Redirect to the products page if not a POST request
@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(MedicalAccessories, pk=product_id)
        try:
            cart_item = CartItem.objects.get(user=user, accessory=product)
            cart_item.delete()
            messages.success(request, "Item removed from your cart.")
        except CartItem.DoesNotExist:
            messages.error(request, "Item not found in your cart.")

    return redirect('cart')

def update_cart(request, product_id):
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(MedicalAccessories, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))

        try:
            cart_item = CartItem.objects.get(user=user, accessory=product)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.total_cost = cart_item.quantity * cart_item.accessory.p_cost
                cart_item.save()
                messages.success(request, "Cart item updated.")
            else:
                cart_item.delete()
                messages.success(request, "Item removed from your cart.")
        except CartItem.DoesNotExist:
            messages.error(request, "Item not found in your cart.")

    return redirect('cart')