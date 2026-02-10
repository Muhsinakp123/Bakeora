from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Subscriber,CustomerProfile

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST['username']
        password = request.POST['password']

        # Allow login via username or email
        try:
            user_obj = User.objects.get(email=username_or_email)
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username/email or password")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # ✅ create customer profile
            CustomerProfile.objects.create(user=user)

            # ✅ IMPORTANT: specify backend
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('home')

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect('home')

def subscribe_email(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            Subscriber.objects.get_or_create(email=email)

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def my_orders(request):
    return render(request, "my_orders.html")


@login_required
def account_dashboard(request):
    return render(request, "account_dashboard.html")