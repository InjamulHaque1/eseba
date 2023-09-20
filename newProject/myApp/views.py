from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def products(request):
    return render(request, "products.html")

def appointment(request):
    return render(request, "appointment.html")

def about(request):
    return render(request, "about.html")

def emergency(request):
    return render(request, "emergency.html")

