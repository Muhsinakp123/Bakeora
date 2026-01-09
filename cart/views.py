from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .utils import get_or_create_cart
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from products.models import ProductSearch

# Create your views here.


@login_required(login_url='login')
def cart_view(request):
    cart = get_or_create_cart(request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(ProductSearch, id=product_id)
    cart = get_or_create_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
    item.save()

    messages.success(request, "Product added to cart")
    return redirect('shop')