from datetime import timedelta
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncDate
import json

from orders.models import Order


def admin_dashboard(request):

    # 1️⃣ Total Revenue (Delivered only)
    total_revenue = (
        Order.objects
        .filter(status='delivered')
        .aggregate(total=Sum('total_amount'))['total'] or 0
    )

    # 2️⃣ Stats Cards
    shipped_orders = Order.objects.filter(status='delivered').count()

    pending_orders = Order.objects.filter(
        status__in=['placed', 'preparing']
    ).count()

    new_orders_today = Order.objects.filter(
        created_at__date=timezone.now().date()
    ).count()

    # 3️⃣ Recent Activity
    recent_activity = Order.objects.order_by('-created_at')[:5]

    # 4️⃣ Last 7 Days Sales Chart
    last_week = timezone.now() - timedelta(days=6)

    sales_data = (
        Order.objects
        .filter(created_at__gte=last_week, status='delivered')
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total=Sum('total_amount'))
        .order_by('date')
    )

    chart_labels = [entry['date'].strftime('%b %d') for entry in sales_data]
    chart_values = [entry['total'] for entry in sales_data]

    context = {
        'total_revenue': total_revenue,
        'shipped_orders': shipped_orders,
        'pending_orders': pending_orders,
        'new_orders_today': new_orders_today,
        'recent_activity': recent_activity,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
    }

    return render(request, 'adminpanel/dashboard.html', context)
