from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.db.models import Sum
from orders.models import Order, OrderItem

def admin_dashboard(request):
    total_orders = Order.objects.count()

    revenue = (
        Order.objects
        .filter(status='delivered')
        .aggregate(total=Sum('total_amount'))
        ['total'] or 0
    )

    pending = Order.objects.exclude(status='delivered').count()

    top_products = (
        OrderItem.objects
        .values('product__name')
        .annotate(qty=Sum('quantity'))
        .order_by('-qty')[:5]
    )

    context = {
        'total_orders': total_orders,
        'revenue': revenue,
        'pending': pending,
        'top_products': top_products,
    }

    return render(request, 'adminpanel/dashboard.html', context)
