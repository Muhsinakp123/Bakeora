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
from django.contrib.auth.decorators import login_required, user_passes_test

def admin_check(user):
    return user.is_superuser

def admin_required(view_func):
    @login_required(login_url='login')
    @user_passes_test(admin_check, login_url='login')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
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

@admin_required
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'All Orders'
    })
    
@admin_required
def admin_order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()

    return render(request, "adminpanel/order_detail.html", {
        "order": order,
        "items": items
    })
    
@admin_required   
def update_order_status(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        status = request.POST.get("status")
        order.status = status
        order.save()

    return redirect(request.META.get("HTTP_REFERER"))

@admin_required
def pending_orders(request):
    orders = Order.objects.filter(status='pending').order_by('-created_at')

    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'Pending Orders'
    })

@admin_required
def preparing_orders(request):
    orders = Order.objects.filter(status='preparing').order_by('-created_at')

    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'Preparing Orders'
    })
    
@admin_required    
def out_for_delivery_orders(request):
    orders = Order.objects.filter(status='out_for_delivery').order_by('-created_at')

    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'Out for Delivery'
    })
    
@admin_required
def delivered_orders(request):
    orders = Order.objects.filter(status='delivered').order_by('-created_at')

    return render(request,'adminpanel/orders.html',{
        'orders':orders,
        'title':'Delivered Orders'
    })
    
@admin_required    
def admin_custom_cake_detail(request, cake_id):

    cake = get_object_or_404(CustomCake, id=cake_id)

    return render(request, "adminpanel/custom_cake_detail.html", {
        "cake": cake,
        "title": "Cake Request Details"
    })  
      
@admin_required        
def custom_cakes_pending(request):
    cakes = CustomCake.objects.filter(status='pending').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'New Cake Requests'
    })

@admin_required
def custom_cakes_quoted(request):
    cakes = CustomCake.objects.filter(status='quoted').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Quoted Cakes'
    })

@admin_required
def custom_cakes_confirmed(request):
    cakes = CustomCake.objects.filter(status='confirmed').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Confirmed Cakes'
    })

@admin_required
def custom_cakes_baking(request):
    cakes = CustomCake.objects.filter(status='baking').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Baking Cakes'
    })

@admin_required
def custom_cakes_delivery(request):
    cakes = CustomCake.objects.filter(status='out_for_delivery').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Out for Delivery'
    })

@admin_required
def custom_cakes_delivered(request):
    cakes = CustomCake.objects.filter(status='delivered').order_by('-created_at')

    return render(request,'adminpanel/custom_cakes.html',{
        'cakes':cakes,
        'title':'Delivered Cakes'
    })   
  
@admin_required    
def update_custom_cake_status(request, cake_id):

    cake = get_object_or_404(CustomCake, id=cake_id)

    if request.method == "POST":
        status = request.POST.get("status")
        cake.status = status
        cake.save()

    return redirect(request.META.get("HTTP_REFERER"))

@admin_required 
def admin_cakes(request):

    products = Cake.objects.all().order_by('-id')

    return render(request, "adminpanel/products.html", {
        "products": products,
        "title": "Cakes",
        "type": "cake"
    })

@admin_required 
def admin_desserts(request):

    products = Dessert.objects.all().order_by('-id')

    return render(request, "adminpanel/products.html", {
        "products": products,
        "title": "Desserts",
        "type": "dessert"
    })

@admin_required 
def admin_puddings(request):

    products = Pudding.objects.all().order_by('-id')

    return render(request, "adminpanel/products.html", {
        "products": products,
        "title": "Puddings",
        "type": "pudding"
    })
    
@admin_required    
def add_product(request, type):

    if request.method == "POST":

        name = request.POST.get("name")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        if type == "cake":

            Cake.objects.create(
                name=name,
                price=price,
                image=image,
                category=request.POST.get("category"),
                flavor=request.POST.get("flavor"),
                structure=request.POST.get("structure")
            )

        elif type == "dessert":

            Dessert.objects.create(
                name=name,
                price=price,
                image=image,
                category=request.POST.get("category"),
                flavor=request.POST.get("flavor")
            )

        elif type == "pudding":

            Pudding.objects.create(
                name=name,
                price=price,
                image=image,
                flavor=request.POST.get("flavor"),
                style=request.POST.get("style"),
            )

        return redirect(f"/adminpanel/products/{type}s/")

    return render(request,"adminpanel/add_product.html",{
        "type":type
    }) 
      
@admin_required    
def edit_product(request, type, id):

    if type == "cake":
        model = Cake
    elif type == "dessert":
        model = Dessert
    else:
        model = Pudding

    product = get_object_or_404(model,id=id)

    if request.method == "POST":

        product.name = request.POST.get("name")
        product.price = request.POST.get("price")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()

        return redirect(f"/adminpanel/products/{type}s/")

    return render(request,"adminpanel/edit_product.html",{
        "product":product,
        "type":type
    }) 
      
@admin_required    
def delete_product(request,type,id):

    if type == "cake":
        model = Cake
    elif type == "dessert":
        model = Dessert
    else:
        model = Pudding

    product = get_object_or_404(model,id=id)
    product.delete()

    return redirect(f"/adminpanel/products/{type}s/")     

@admin_required
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
    
@admin_required    
def subscribers_list(request):
    subscribers = Subscriber.objects.all().order_by('-created_at')

    return render(request, 'adminpanel/subscribers.html', {
        'subscribers': subscribers,
        'title': 'Subscribers'
    })