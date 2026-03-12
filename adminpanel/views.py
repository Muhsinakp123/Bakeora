from datetime import timedelta
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Sum,Count
from django.utils import timezone
from django.db.models.functions import TruncDate
import json
from django.contrib.auth.models import User
from products.models import ProductSearch
from orders.models import Order,CustomCake,OrderItem
from products.models import Cake, Dessert, Pudding
from accounts.models import Subscriber


def admin_dashboard(request):
    
    customers = User.objects.filter(is_superuser=False).count()
    products = ProductSearch.objects.count()

    # 1️⃣ Total Revenue (Delivered only)
    total_revenue = (
        Order.objects
        .filter(status='delivered')
        .aggregate(total=Sum('total_amount'))['total'] or 0
    )

    # 2️⃣ Stats Cards
    shipped_orders = Order.objects.filter(status='delivered').count()

    pending_orders = Order.objects.filter(
        status__in=['pending','paid','preparing']
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
    
    # District-wise orders
    
    district_data = (
    Order.objects
    .values('address__district')
    .annotate(total=Count('id'))
)
    
    district_labels = [d['address__district'] for d in district_data]
    district_values = [d['total'] for d in district_data]
    
    total_orders = Order.objects.count()

    delivered_orders = Order.objects.filter(status='delivered').count()
    preparing_orders = Order.objects.filter(status='preparing').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()

    # Convert to percentage
    delivery_percent = round((delivered_orders / total_orders) * 100) if total_orders else 0
    prepare_percent = round((preparing_orders / total_orders) * 100) if total_orders else 0
    cancel_percent = round((cancelled_orders / total_orders) * 100) if total_orders else 0
    
    top_products = (
        OrderItem.objects
        .filter(order__status='delivered')
        .values('product_name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )
    
    top_products_list = [
        {
            "name": item['product_name'],
            "count": item['total_sold']
        }
        for item in top_products
    ]
    
    context = {
        'total_revenue': total_revenue,
        'shipped_orders': shipped_orders,
        'pending_orders': pending_orders,
        'new_orders_today': new_orders_today,
        'recent_activity': recent_activity,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'district_labels': json.dumps(district_labels),
        'district_values': json.dumps(district_values),
        'customers': customers,
        'products': products,
        'delivery_percent': delivery_percent,
        'prepare_percent': prepare_percent,
        'cancel_percent': cancel_percent,
        'top_products': top_products_list,
    }

    return render(request, 'adminpanel/dashboard.html', context)


def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'All Orders'
    })
    

def admin_order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()

    return render(request, "adminpanel/order_detail.html", {
        "order": order,
        "items": items
    })
    
def update_order_status(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        status = request.POST.get("status")
        order.status = status
        order.save()

    return redirect(request.META.get("HTTP_REFERER"))

def pending_orders(request):
    orders = Order.objects.filter(status='pending').order_by('-created_at')

    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'Pending Orders'
    })


def preparing_orders(request):
    orders = Order.objects.filter(status='preparing').order_by('-created_at')

    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'Preparing Orders'
    })
    
def out_for_delivery_orders(request):
    orders = Order.objects.filter(status='out_for_delivery').order_by('-created_at')

    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'Out for Delivery'
    })

def delivered_orders(request):
    orders = Order.objects.filter(status='delivered').order_by('-created_at')

    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'Delivered Orders'
    })
    
def admin_custom_cake_detail(request, cake_id):

    cake = get_object_or_404(CustomCake, id=cake_id)

    return render(request, "adminpanel/custom_cake_detail.html", {
        "cake": cake,
        "title": "Cake Request Details"
    })    
        
def custom_cakes_pending(request):
    cakes = CustomCake.objects.filter(status='pending').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'New Cake Requests'
    })


def custom_cakes_quoted(request):
    cakes = CustomCake.objects.filter(status='quoted').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Quoted Cakes'
    })


def custom_cakes_confirmed(request):
    cakes = CustomCake.objects.filter(status='confirmed').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Confirmed Cakes'
    })


def custom_cakes_baking(request):
    cakes = CustomCake.objects.filter(status='baking').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Baking Cakes'
    })


def custom_cakes_delivery(request):
    cakes = CustomCake.objects.filter(status='out_for_delivery').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Out for Delivery'
    })


def custom_cakes_delivered(request):
    cakes = CustomCake.objects.filter(status='delivered').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Delivered Cakes'
    })    

def products_list(request):

    cakes = Cake.objects.all()
    desserts = Dessert.objects.all()
    puddings = Pudding.objects.all()

    context = {
        "cakes": cakes,
        "desserts": desserts,
        "puddings": puddings,
    }

    return render(request,"adminpanel/products.html",context)


def customers_list(request):
    customers = User.objects.filter(
        is_superuser=False
    ).annotate(
        total_orders=Count('order')
    ).order_by('-date_joined')

    return render(request, 'adminpanel/customers.html', {
        'customers': customers,
        'title': 'Customers'
    })
    
def subscribers_list(request):
    subscribers = Subscriber.objects.all().order_by('-created_at')

    return render(request, 'adminpanel/subscribers.html', {
        'subscribers': subscribers,
        'title': 'Subscribers'
    })