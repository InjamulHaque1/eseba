from django.utils import timezone
from django.urls import reverse
from .models import *
from django.shortcuts import (
    get_object_or_404, 
    redirect, 
    render
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate, 
    login as auth_login, 
    logout as auth_logout
)
from .forms import UserProfileForm, UserForm
from django.db.models import Q 

def home(request):
    return render(request, "home.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("u_name")
        password = request.POST.get("u_password")
        
        authenticated_user = authenticate(request, username=username, password=password)       
        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, f"Welcome, {username}!")
            return redirect("home")
        
        else:
            messages.error(request, "Try again!")

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
        user = User.objects.create_user(username=u_name, email=u_email, password=u_password)
        user.save()
        user_profile = UserProfile(user=user, age=u_age, address=u_address, mobile=u_mobile, gender=u_gender)
        user_profile.save()
        
        authenticated_user = authenticate(username=u_name, password=u_password)
        
        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, "Your account has been successfully created.")
            return redirect("home")
        user = User.objects.create_user(username=u_name, email=u_email, password=u_password)
        user.save()
        user_profile = UserProfile(user=user, age=u_age, address=u_address, mobile=u_mobile, gender=u_gender)
        user_profile.save()
        
        authenticated_user = authenticate(username=u_name, password=u_password)
        
        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, "Your account has been successfully created.")
            return redirect("home")

    return render(request, "register.html")

@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_form = UserProfileForm(instance=user_profile)
    user_form = UserForm(instance=request.user)

    if request.method == "POST":
        if "delete_account" in request.POST:
            request.user.delete()
            auth_logout(request)
            messages.success(request, "Your account has been deleted.")
            return redirect('login')

        profile_form = UserProfileForm(request.POST, instance=user_profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')
        else:
            messages.error(request, "Error updating profile. Please check the form.")

    context = {
        'user_profile': user_profile,
        'profile_form': profile_form,
        'user_form': user_form,
        }
    return render(request, 'user_profile.html', context)

@login_required
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
        products = MedicalAccessories.objects.filter(
            Q(p_name__icontains=query) | Q(p_description__icontains=query)
        )
    else:
        messages.error(request, "Search bar was empty")
        products = MedicalAccessories.objects.all()

    context = {
        'products': products,
        }

    return render(request, 'products.html', context)

@login_required
def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    for item in cart_items:
        item.total_cost = item.accessory.p_cost * item.quantity
        
        
    total_cost = sum(item.total_cost for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost
        }
    return render(request, 'cart.html', context)

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

        cart_item, created = CartItem.objects.get_or_create(user=user, accessory=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
            
        cart_item.total_cost = cart_item.quantity * cart_item.accessory.p_cost
        cart_item.save()
        messages.success(request, "Successfully added")
        return redirect(reverse('products'))
    else:
        return redirect('products') 

@login_required
def remove_from_cart(request, product_id):
    
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(MedicalAccessories, pk=product_id)
        cart_item = CartItem.objects.get(user=user, accessory=product)
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
    return redirect('cart')

@login_required
def update_cart(request, product_id):
    
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(MedicalAccessories, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item = CartItem.objects.get(user=user, accessory=product)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.total_cost = cart_item.quantity * cart_item.accessory.p_cost
            cart_item.save()
            messages.success(request, "Cart item updated.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from your cart.")
        cart_item = CartItem.objects.get(user=user, accessory=product)
        
    return redirect('cart')

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    
    total_cost = 0
    for item in cart_items:
        total_cost += item.total_cost
    
    for item in cart_items:
        if item.accessory.p_count >= item.quantity:
            item.accessory.p_count -= item.quantity
            item.accessory.save()

        new_bill = Bill(
            customer=user,
            total_cost=item.total_cost,
            created_at=timezone.now(), 
            quantity=item.quantity, 
            accessory=item.accessory,
        )
        new_bill.save()
    messages.success(request, "Checkout successful.")
    cart_items.delete()
    
    context ={
        'bill_items': cart_items
        }

    return render(request, 'checkout.html', context)

def appointment(request):
    doctors = Doctor.objects.all()
    context = {
        'doctors': doctors
    }
    return render(request, "appointment.html", context)

def doctor_search(request):
    query_d = request.GET.get('q')
    
    if query_d:
        doctors = Doctor.objects.filter(
            Q(name__icontains=query_d)
        )
    else:
        messages.error(request, "Search bar was empty")
        doctors = Doctor.objects.all()

    context = {
        'doctors': doctors,
        }

    return render(request, 'appointment.html', context)

@login_required
def create_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    
    if request.method == 'POST':
        appointment_date = request.POST['appointment_date']
        description = request.POST['description']
        appointment_time_id = request.POST['appointment_time']
        time_slot = DoctorTimeSlot.objects.get(id=appointment_time_id, doctor=doctor)
        
        selected_date = timezone.datetime.strptime(appointment_date, '%Y-%m-%d').date()

        today = timezone.now().date()
        if selected_date < today:
            messages.error(request, "Please select an upcoming date.")
            return redirect(reverse('create_appointment', args=[doctor_id]))

        if doctor.available_spots == 0:
            doctor.status = False
            doctor.save()
        
        appointment = Appointment(
            user=request.user,
            doctor=doctor,
            appointment_date=appointment_date,
            description=description,
            doctor_time_slot=time_slot
        )
        appointment.save()
        doctor.available_spots -= 1
        doctor.save()
        messages.success(request, "Successful appointment made")
        return redirect(reverse('appointment'))
        
    context ={
        'doctor': doctor
    }
    return render(request, 'create_appointment.html', context)

def about(request):
    return render(request, "about.html")

def emergency(request):
    return render(request, "emergency.html")