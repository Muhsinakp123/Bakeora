from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import ProductSearch
from .models import CartItem
from .utils import get_or_create_cart


def cart_view(request):

    # ---------- GUEST ----------
    if not request.user.is_authenticated:
        session_cart = request.session.get("cart", {})
        session_total = sum(
            i["price"] * i["quantity"]
            for i in session_cart.values()
        )

        return render(request, "cart.html", {
            "session_cart": session_cart,
            "session_total": session_total,
            "db_cart": None
        })

    # ---------- USER ----------
    db_cart = get_or_create_cart(request.user)
    items = db_cart.items.select_related("product")

    db_cart.total_price = sum(
        i.total_price for i in items   # uses property correctly
    )

    return render(request, "cart.html", {
        "db_cart": db_cart,
        "session_cart": None,
        "session_total": 0
    })

# ================= ADD =================

@require_POST
def add_to_cart(request, product_id):

    product = get_object_or_404(ProductSearch, id=product_id)

    # -------- GUEST --------
    if not request.user.is_authenticated:
        cart = request.session.get("cart", {})
        pid = str(product.id)

        if pid in cart:
            cart[pid]["quantity"] += 1
        else:
            cart[pid] = {
                "name": product.name,
                "price": float(product.price),
                "quantity": 1,
                "image": product.image.url if product.image else ""
            }

        request.session["cart"] = cart
        request.session.modified = True

        cart_count = sum(i["quantity"] for i in cart.values())

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "cart_count": cart_count
            })

        return redirect("cart")

    # -------- USER --------
    cart = get_or_create_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
    item.save()

    cart_count = sum(i.quantity for i in cart.items.all())

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "cart_count": cart_count
        })

    return redirect("cart")

def update_cart_qty(request, product_id):
    action = request.POST.get("action")

    item = CartItem.objects.get(
        cart__user=request.user,
        product_id=product_id
    )

    if action == "plus":
        item.quantity += 1
    elif action == "minus":
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return JsonResponse({"removed": True})

    item.save()

    return JsonResponse({"success": True})


# ================= REMOVE =================

def remove_from_cart(request, product_id):

    if not request.user.is_authenticated:
        cart = request.session.get("cart", {})
        cart.pop(str(product_id), None)
        request.session["cart"] = cart
        request.session.modified = True
        return redirect("cart")

    CartItem.objects.filter(
        cart__user=request.user,
        product_id=product_id
    ).delete()

    return redirect("cart")
