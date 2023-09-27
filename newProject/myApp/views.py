from django.utils import timezone
from sqlite3 import IntegrityError
from django.db import transaction
from django.urls import reverse
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserForm
from django.db.models import Q 

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
            user.save()
            user_profile = UserProfile(user=user, age=u_age, address=u_address, mobile=u_mobile, gender=u_gender)
            user_profile.save()
            
            authenticated_user = authenticate(username=u_name, password=u_password)
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                messages.success(request, "Your account has been successfully created.")
                return redirect("home")
        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect("register")

    return render(request, "register.html")

def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        if "delete_account" in request.POST:
            user_profile.delete()
            auth_logout(request)
            messages.success(request, "Your account has been deleted.")
            return redirect('login')

        profile_form = UserProfileForm(request.POST, instance=user_profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('home')
        else:
            messages.error(request, "Error updating profile. Please check the form.")
    else:
        profile_form = UserProfileForm(instance=user_profile)
        user_form = UserForm(instance=request.user)

    return render(request, 'user_profile.html', {'user_profile': user_profile, 'profile_form': profile_form, 'user_form': user_form})

def logout(request):
    user = request.user
    CartItem.objects.filter(user=user).delete()
    
    auth_logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('home')

def products(request):
    products = MedicalAccessories.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products.html', context)

def product_search(request):
    query = request.GET.get('q')
    
    if query:
        # Perform a case-insensitive search on product names and descriptions
        products = MedicalAccessories.objects.filter(
            Q(p_name__icontains=query) | Q(p_description__icontains=query)
        )
    else:
        messages.error(request, "No product found...")
        products = MedicalAccessories.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products.html', context)

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
        quantity = int(request.POST.get('quantity', 0))

        if quantity <= 0:
            messages.error(request, "Add at least 1 item!")
            return redirect(reverse('products'))
        
        if quantity > product.p_count:
            messages.error(request, "Out of stock!")
            return redirect(reverse('products'))

        # Check if the item is already in the cart for the user
        cart_item, created = CartItem.objects.get_or_create(user=user, accessory=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.total_cost = cart_item.quantity * cart_item.accessory.p_cost  # Calculate the total cost
        cart_item.save()
        messages.success(request, "Successfully added")
        return redirect(reverse('products'))
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

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    
    # Calculate the total cost
    total_cost = 0
    for item in cart_items:
        total_cost += item.total_cost
    
    context = {
        'bill_items': cart_items,  # Pass cart_items to the checkout template
        'total_cost': total_cost,
    }

    with transaction.atomic():
        for item in cart_items:
            # Check stock availability
            if item.accessory.p_count >= item.quantity:
                item.accessory.p_count -= item.quantity
                item.accessory.save()

            new_bill = Bill(
                customer=user,  # Replace with actual customer information
                total_cost=item.total_cost,
                created_at=timezone.now(),  # Save the current time
                quantity=item.quantity,  # Save quantity
                accessory=item.accessory,  # Link the accessory to the bill
            )
            new_bill.save()
        
        messages.success(request, "Checkout successful.")

    # Clear the user's cart after the transaction is completed
    cart_items.delete()

    return render(request, 'checkout.html', {'bill_items': cart_items})

def appointment(request):
    return render(request, "appointment.html")

def about(request):
    return render(request, "about.html")

def emergency(request):
    return render(request, "emergency.html")