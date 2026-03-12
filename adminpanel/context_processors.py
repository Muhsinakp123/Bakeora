from orders.models import Order,CustomCake

def admin_counts(request):
    return {
        'pending_count': Order.objects.filter(status='pending').count(),
        'preparing_count': Order.objects.filter(status='preparing').count(),
        'out_delivery_count': Order.objects.filter(status='out_for_delivery').count(),
        'delivered_count': Order.objects.filter(status='delivered').count(),
        'all_orders_count': Order.objects.count(),

        'cakes_pending_count': CustomCake.objects.filter(status='pending').count(),
        'cakes_quoted_count': CustomCake.objects.filter(status='quoted').count(),
        'cakes_confirmed_count': CustomCake.objects.filter(status='confirmed').count(),
        'cakes_baking_count': CustomCake.objects.filter(status='baking').count(),
        'cakes_delivery_count': CustomCake.objects.filter(status='out_for_delivery').count(),
        'cakes_delivered_count': CustomCake.objects.filter(status='delivered').count(),
    }