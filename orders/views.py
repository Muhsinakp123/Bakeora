from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import CustomCake, Order, OrderItem, Address
from cart.models import Cart, CartItem
from products.models import Cake, Dessert, Pudding


# ===================== CUSTOM CAKE =====================

@login_required(login_url='login')
def custom_order(request):
    if request.method == "POST":
        order = CustomCake.objects.create(
            user=request.user,
            cake_type=request.POST.get('cake_type'),
            size=request.POST.get('size'),
            flavor=request.POST.get('flavor'),
            cream_type=request.POST.get('cream_type'),
            message_on_cake=request.POST.get('message_on_cake'),
            reference_photo=request.FILES.get('reference_image'),
            delivery_datetime=request.POST.get('delivery_date'),
            delivery_address=request.POST.get('delivery_address'),
            notes=request.POST.get('notes'),
            status="pending"
        )
        return redirect('custom_checkout', order_id=order.id)

    return render(request, 'custom_order.html')


@login_required
def custom_checkout(request, order_id):
    order = get_object_or_404(CustomCake, id=order_id, user=request.user)
    return render(request, "custom_checkout.html", {"order": order})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})


# ===================== CART CHECKOUT =====================

@login_required(login_url='login')
def checkout(request):

    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect('cart')

    addresses = Address.objects.filter(user=request.user)

    if not addresses.exists():
        return redirect('add_address')

    total = sum(
        item.product.price * item.quantity
        for item in cart.items.all()
    )

    return render(request, 'checkout.html', {
        'cart_items': cart.items.all(),
        'total': total,
        'addresses': addresses,
    })


@login_required(login_url='login')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})


# ===================== BUY NOW FLOW =====================

@login_required(login_url='login')
def buy_now(request, product_type, product_id):
    request.session['buy_product_type'] = product_type.strip().lower()
    request.session['buy_product_id'] = product_id

    return redirect(
        "buy_now_address_with_product",
        product_type=product_type,
        product_id=product_id
    )


@login_required(login_url='login')
def buy_now_address(request, product_type, product_id):

    MODEL_MAP = {
        "cake": Cake,
        "dessert": Dessert,
        "pudding": Pudding,
        "custom": CustomCake,
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
        "custom": CustomCake,
    }

    model = MODEL_MAP.get(product_type.strip().lower())

    if not model:
        return redirect("shop")

    product = get_object_or_404(model, id=product_id)
    address = get_object_or_404(Address, id=address_id, user=request.user)

    price = product.price
    name = product.name if product_type != "custom" else f"Custom Cake - {product.flavor}"

    order = Order.objects.create(
        user=request.user,
        address=address,
        total_amount=price
    )

    OrderItem.objects.create(
        order=order,
        product_name=name,
        price=price,
        quantity=1
    )

    # ✅ Proper linking for Custom Cake
    if product_type == "custom":
        product.status = "confirmed"
        product.order = order   # Correct linking
        product.save()

    request.session['order_id'] = order.id

    return redirect("payment_page")


@login_required(login_url='login')
def add_address(request):

    product_type = request.session.get('buy_product_type')
    product_id = request.session.get('buy_product_id')

    if request.method == "POST":

        city = request.POST.get("city", "").strip().lower()

        #  Validate allowed districts
        if city not in settings.ALLOWED_DISTRICTS:
            messages.error(
                request,
                "Sorry! Bakeora currently delivers only to "
                "Kozhikode, Kannur, Malappuram, and Wayanad."
            )
            return redirect("add_address")

        # Save only if valid
        Address.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            city=request.POST.get("city"),
            pincode=request.POST.get("pincode"),
            address_line=request.POST.get("address_line"),
        )

        if product_type and product_id:
            return redirect(
                "buy_now_address_with_product",
                product_type=product_type,
                product_id=product_id
            )

        return redirect("checkout")

    return render(request, "add_address.html")


# ===================== PAYMENT =====================

@login_required
def payment_success(request):

    order_id = request.session.get("order_id")

    if not order_id:
        messages.error(request, "No order found.")
        return redirect("shop")

    order = get_object_or_404(Order, id=order_id, user=request.user)

    # ✅ Mark order as paid
    order.status = "paid"
    order.save()

    # ✅ If custom cake linked
    custom_cake = CustomCake.objects.filter(order=order).first()
    if custom_cake:
        custom_cake.payment_status = "paid"
        custom_cake.status = "confirmed"
        custom_cake.save()

    # ✅ Clear cart
    CartItem.objects.filter(cart__user=request.user).delete()

    # ✅ Clear session
    if "order_id" in request.session:
        del request.session["order_id"]

    if "buy_product_type" in request.session:
        del request.session["buy_product_type"]

    if "buy_product_id" in request.session:
        del request.session["buy_product_id"]

    messages.success(request, "Payment successful!")

    return redirect("order_success", order_id=order.id)


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


@login_required
def my_orders(request):

    # Regular orders = Orders NOT linked to any CustomCake
    normal_orders = Order.objects.filter(
        user=request.user,
        custom_cakes__isnull=True
    ).order_by("-created_at")

    #  Custom orders
    custom_orders = CustomCake.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "my_orders.html", {
        "normal_orders": normal_orders,
        "custom_orders": custom_orders
    })


@login_required
def custom_pay_now(request, order_id):
    custom_order = get_object_or_404(
        CustomCake,
        id=order_id,
        user=request.user
    )

    if custom_order.status != "quoted" or not custom_order.price:
        messages.error(request, "Price not confirmed yet.")
        return redirect("custom_checkout", order_id=order_id)

    if custom_order.payment_status == "paid":
        messages.success(request, "Already paid.")
        return redirect("custom_checkout", order_id=order_id)

    # Save session for payment flow
    request.session['buy_product_type'] = "custom"
    request.session['buy_product_id'] = custom_order.id

    return redirect(
        "buy_now_address_with_product",
        product_type="custom",
        product_id=custom_order.id
    )


@login_required
def proceed_payment(request, address_id):

    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect('cart')

    address = get_object_or_404(Address, id=address_id, user=request.user)

    # ✅ District validation
    if address.city.strip().lower() not in settings.ALLOWED_DISTRICTS:
        messages.error(
            request,
            " Sorry! Bakeora currently delivers only to "
            "Kozhikode, Kannur, Malappuram, and Wayanad."
        )
        return redirect("checkout")

    total = sum(
        item.product.price * item.quantity
        for item in cart.items.all()
    )

    # ✅ Create order
    order = Order.objects.create(
        user=request.user,
        address=address,
        total_amount=total
    )

    # ✅ Create order items
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )

    request.session['order_id'] = order.id

    return redirect("payment_page")