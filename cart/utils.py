from .models import Cart, CartItem
from products.models import ProductSearch

def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def merge_session_cart_to_db(request, user):
    session_cart = request.session.get('cart')

    if not session_cart:
        return

    cart = get_or_create_cart(user)

    for product_id, item in session_cart.items():
        product = ProductSearch.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += item['quantity']
        else:
            cart_item.quantity = item['quantity']

        cart_item.save()

    # Clear session cart after merge
    del request.session['cart']
    request.session.modified = True
