from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import ProductSearch
from .models import CartItem
from .utils import get_or_create_cart
from django.contrib.auth.decorators import login_required


# Create your views here.


def cart_view(request):

    # 🟡 GUEST CART
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        total = sum(
            item['price'] * item['quantity']
            for item in cart.values()
        )
        return render(request, 'cart.html', {
            'session_cart': cart,
            'total': total
        })

    # 🟢 USER CART
    cart = get_or_create_cart(request.user)
    return render(request, 'cart.html', {
        'db_cart': cart
    })



def add_to_cart(request, product_id):
    product = get_object_or_404(ProductSearch, id=product_id)

    # 🟡 GUEST USER → SESSION CART
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        pid = str(product.id)

        if pid in cart:
            cart[pid]['quantity'] += 1
        else:
            cart[pid] = {
                'name': product.name,
                'price': product.price,
                'quantity': 1,
                'image': product.image.url
            }

        request.session['cart'] = cart
        request.session.modified = True

        messages.success(request, "Added to cart")
        return redirect('cart')

    # 🟢 LOGGED-IN USER → DB CART
    cart = get_or_create_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
    item.save()

    messages.success(request, "Added to cart")
    return redirect('cart')


def remove_from_cart(request, product_id):

    # GUEST
    if not request.user.is_authenticated:
        cart = request.session.get('cart', {})
        pid = str(product_id)
        if pid in cart:
            del cart[pid]
            request.session.modified = True
        return redirect('cart')

    # USER
    item = get_object_or_404(
        CartItem,
        cart__user=request.user,
        product_id=product_id
    )
    item.delete()
    return redirect('cart')

