from cart.models import Cart

def cart_count(request):

    # ---------- LOGGED USER ----------
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return {"cart_count": cart.items.count()}
        return {"cart_count": 0}

    # ---------- GUEST USER ----------
    session_cart = request.session.get("cart", {})
    count = sum(item["quantity"] for item in session_cart.values())

    return {"cart_count": count}
