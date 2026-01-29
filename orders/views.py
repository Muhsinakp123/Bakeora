from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import CustomCakeOrder, Order, OrderItem, Address
from cart.models import Cart,CartItem
from products.models import Cake


# ===================== CUSTOM CAKE =====================

@login_required(login_url='login')
def custom_order(request):
    if request.method == "POST":
        order = CustomCakeOrder.objects.create(
            user=request.user,
            cake_type=request.POST['cake_type'],
            flavor=request.POST['flavor'],
            size=request.POST['size'],
            message_on_cake=request.POST.get('message'),
            delivery_date=request.POST['delivery_date'],
            notes=request.POST.get('notes')
        )
        return redirect('custom_checkout', order_id=order.id)

    return render(request, 'custom_order.html')


@login_required(login_url='login')
def custom_checkout(request, order_id):
    order = get_object_or_404(CustomCakeOrder, id=order_id, user=request.user)

    if request.method == "POST":
        order.status = 'paid'
        order.save()
        messages.success(request, "🎉 Custom cake order placed successfully!")
        return redirect('home')

    return render(request, 'custom_checkout.html', {'order': order})


# ===================== CART CHECKOUT =====================

@login_required(login_url='login')
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect('cart')

    total = sum(
        item.product.price * item.quantity
        for item in cart.items.all()
    )

    if request.method == "POST":
        city = request.POST['city'].strip().lower()

        # 🚫 LOCATION VALIDATION (CRITICAL)
        if city not in settings.ALLOWED_DISTRICTS:
            messages.error(
                request,
                "🚫 Sorry! Bakeora currently delivers only to "
                "Kozhikode, Kannur, Malappuram, and Wayanad."
            )
            return redirect('checkout')

        # ✅ Allowed → continue checkout
        address = Address.objects.create(
            user=request.user,
            full_name=request.POST['name'],
            phone=request.POST['phone'],
            city=request.POST['city'],
            pincode=request.POST['pincode'],
            address_line=request.POST['address']
        )

        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )

        request.session['order_id'] = order.id
        return redirect('payment_page')

    return render(request, 'checkout.html', {
        'cart_items': cart.items.all(),
        'total': total,
        'allowed_districts': settings.ALLOWED_DISTRICTS
    })

@login_required(login_url='login')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})


# ===================== PAYPAL BUY NOW =====================

@login_required(login_url='login')
def buy_now(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)

    context = {
        'cake': cake,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    }

    return render(request, 'payment_page.html', context)


@csrf_exempt
def payment_success(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    order.status = 'paid'
    order.save()

    # ✅ Clear cart
    CartItem.objects.filter(cart__user=order.user).delete()

    del request.session['order_id']

    messages.success(request, "🎉 Order placed successfully!")
    return redirect('order_success', order_id=order.id)


@login_required
def payment_page(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.address.city.lower() not in settings.ALLOWED_DISTRICTS:
        messages.error(request, "Delivery not available in your location")
        return redirect('checkout')

    return render(request, 'payment_page.html', {
        'order': order,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    })

