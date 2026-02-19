from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import CustomCake, Order, OrderItem, Address
from cart.models import Cart,CartItem
from products.models import Cake, Dessert, Pudding


# ===================== CUSTOM CAKE =====================

@login_required(login_url='login')
def custom_order(request):
    if request.method == "POST":
        order = CustomCake.objects.create(
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
    order = get_object_or_404(CustomCake, id=order_id, user=request.user)

    if request.method == "POST":
        order.status = 'paid'
        order.save()
        messages.success(request, " Custom cake order placed successfully!")
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


@login_required(login_url='login')
def buy_now(request, product_type, product_id):

    # Save product info in session
    request.session['buy_product_type'] = product_type.strip().lower()
    request.session['buy_product_id'] = product_id

    return redirect("buy_now_address_with_product", product_type=product_type, product_id=product_id)


@login_required(login_url='login')
def buy_now_address(request, product_type, product_id):

    MODEL_MAP = {
        "cake": Cake,
        "dessert": Dessert,
        "pudding": Pudding,
    }

    model = MODEL_MAP.get(product_type.strip().lower())

    if not model:
        return redirect("shop")

    product = get_object_or_404(model, id=product_id)
    addresses = Address.objects.filter(user=request.user)

    return render(request, "buy_now_address.html", {
        "product": product,
        "addresses": addresses,
        "product_type": product_type,
        "product_id": product_id
    })



@login_required(login_url='login')
def buy_now_create_order(request, address_id, product_type, product_id):

    if request.method != "POST":
        return redirect("shop")

    MODEL_MAP = {
        "cake": Cake,
        "dessert": Dessert,
        "pudding": Pudding,
    }

    model = MODEL_MAP.get(product_type.strip().lower())

    if not model:
        return redirect("shop")

    product = get_object_or_404(model, id=product_id)
    address = get_object_or_404(Address, id=address_id, user=request.user)

    order = Order.objects.create(
        user=request.user,
        address=address,
        total_amount=product.price
    )

    OrderItem.objects.create(
        order=order,
        product_name=product.name,
        price=product.price,
        quantity=1
    )

    request.session['order_id'] = order.id

    return redirect("payment_page")


@login_required(login_url='login')
def add_address(request):

    product_type = request.session.get('buy_product_type')
    product_id = request.session.get('buy_product_id')

    if request.method == "POST":

        Address.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            city=request.POST.get("city"),
            pincode=request.POST.get("pincode"),
            address_line=request.POST.get("address_line"),
        )

        # ✅ If coming from Buy Now flow
        if product_type and product_id:
            return redirect("buy_now_address_with_product", product_type=product_type, product_id=product_id)


        # Otherwise normal flow
        return redirect("checkout")

    return render(request, "add_address.html")


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


@login_required(login_url='login')
def payment_page(request):

    order_id = request.session.get('order_id')

    if not order_id:
        messages.error(request, "No order found.")
        return redirect("shop")

    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "payment_page.html", {
        "order": order,
        "paypal_client_id": settings.PAYPAL_CLIENT_ID
    })




