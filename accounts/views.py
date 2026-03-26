from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Subscriber,CustomerProfile,Notifications
from orders.models import Address, Order, CustomCake
from products.models import Cake, Dessert, Pudding, ProductSearch
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import json
from groq import Groq
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q
import re

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST['username']
        password = request.POST['password']

        # allow login using email
        try:
            user_obj = User.objects.get(email=username_or_email)
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # if admin
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')

            # normal user
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



def get_groq_client():
    api_key = getattr(settings, "GROQ_API_KEY", None)

    if not api_key:
        return None

    return Groq(api_key=api_key)


@csrf_exempt
def bakeora_ai_chatbot(request):

    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request."})

    try:
        data = json.loads(request.body.decode("utf-8"))
        message = data.get("message", "").strip()
        message_lower = message.lower()

    except:
        return JsonResponse({"reply": "Invalid message format."})

    try:

        # ---------------- GREETING ----------------
        if message_lower in ["hi", "hello", "hey"]:
            return JsonResponse({
                "reply": "Hello! Welcome to Bakeora 🍰 How can I help you today?"
            })

        # ---------------- ORDER TRACK ----------------
        if "track" in message_lower or "order status" in message_lower:

            if request.user.is_authenticated:

                order = Order.objects.filter(
                    user=request.user
                ).order_by("-created_at").first()

                if order:
                    reply = f"📦 Your latest order #{order.id} is currently {order.status}."
                else:
                    reply = "You don't have any orders yet."

            else:
                reply = "Please login to check your order status."

            return JsonResponse({"reply": reply})


        # ---------------- CUSTOM CAKE ----------------
        if "custom cake" in message_lower:

            reply = (
                "🎂 You can order a custom cake from our Custom Cake page. "
                "Choose flavor, size and upload your design reference."
            )

            return JsonResponse({"reply": reply})


        # ---------------- PRICE SEARCH ----------------
        price_match = re.search(r"\d+", message_lower)

        if price_match:

            price = int(price_match.group())

            products = ProductSearch.objects.filter(
                price__lte=price
            )[:5]

            if products.exists():

                reply = f"🛒 Here are some items under ₹{price}:\n\n"

                for p in products:
                    reply += f"• {p.name} – ₹{p.price}\n"

            else:
                reply = "Sorry, I couldn't find items in that price range."

            return JsonResponse({"reply": reply})


        # ---------------- PRODUCT SEARCH ----------------
        stop_words = [
            "i", "want", "a", "an", "the", "me",
            "show", "please", "give", "do",
            "you", "have", "need", "for"
        ]

        keywords = [
            word for word in message_lower.split()
            if word not in stop_words
        ]

        products = None

        if keywords:

            query = Q()

            for word in keywords:
                query |= Q(name__icontains=word)

            products = ProductSearch.objects.filter(query)[:5]


        # ---------------- AI RESPONSE ----------------
        product_text = ""

        if products and products.exists():

            for p in products:
                product_text += f"{p.name} – ₹{p.price}\n"

        ai_prompt = f"""
User message:
{message}

Products found in bakery database:
{product_text}

Instructions:
- Reply like a friendly bakery assistant.
- If products exist, recommend them naturally.
- If not, just chat normally.
- Keep reply short and clean.
"""
        client = get_groq_client()
        if not client:
            return JsonResponse({
                "reply": "AI service not configured."
            })
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are Bakeora bakery AI assistant."
                },
                {
                    "role": "user",
                    "content": ai_prompt
                }
            ]
        )

        reply = chat.choices[0].message.content.strip()

        return JsonResponse({"reply": reply})

    except Exception as e:

        print("AI ERROR:", e)

        return JsonResponse({
            "reply": "Sorry, the AI is temporarily unavailable."
        })