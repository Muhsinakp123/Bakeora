from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Subscriber,CustomerProfile,Notifications
from orders.models import Address, Order, CustomCake
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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
def notifications(request):
    notifications = Notifications.objects.filter(
        user=request.user
    ).order_by("-created_at")

    notifications.filter(is_read=False).update(is_read=True)

    return render(request, "notifications.html", {
        "notifications": notifications
    })

@login_required
def get_notification_count(request):
    count = Notifications.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return JsonResponse({"count": count})    

@login_required
def account_dashboard(request):
    return render(request, "account_dashboard.html")


@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "Profile updated successfully!")

    total_orders = Order.objects.filter(user=user).count()
    custom_orders = CustomCake.objects.filter(user=user).count()
    total_addresses = Address.objects.filter(user=user).count()

    context = {
        "total_orders": total_orders,
        "custom_orders": custom_orders,
        "total_addresses": total_addresses,
    }

    return render(request, "profile.html", context)

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "address_list.html", {"addresses": addresses})

@login_required
def custom_cake_orders(request):
    orders = CustomCake.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "custom_cake_order.html", {"orders": orders})

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "change_password.html", {"form": form})