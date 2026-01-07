from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .models import Cake,Dessert,Pudding,ProductSearch
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'home.html')

def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST['username']
        password = request.POST['password']

        # Allow login via username or email
        try:
            user_obj = User.objects.get(email=username_or_email)
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username/email or password")

    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Account created successfully")
            return redirect('login')

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect('home')

def cakes(request):
    cakes = Cake.objects.all()

    # -------- FILTERS --------
    category = request.GET.get('category')
    flavor = request.GET.get('flavor')
    structure = request.GET.get('structure')
    price = request.GET.get('price')

    if category:
        cakes = cakes.filter(category=category)

    if flavor:
        cakes = cakes.filter(flavor=flavor)

    if structure:
        cakes = cakes.filter(structure=structure)

    # -------- PRICE FILTER --------
    if price == '300-600':
        cakes = cakes.filter(price__gte=300, price__lte=600)

    elif price == '500-1000':
        cakes = cakes.filter(price__gte=500, price__lte=1000)

    elif price == '1000-1500':
        cakes = cakes.filter(price__gte=1000, price__lte=1500)

    elif price == 'low-high':
        cakes = cakes.order_by('price')

    elif price == 'high-low':
        cakes = cakes.order_by('-price')

    # -------- PAGINATION (8 items) --------
    paginator = Paginator(cakes, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_cakes': cakes.count()
    }

    return render(request, 'cakes.html', context)

def puddings(request):
    puddings = Pudding.objects.all()

    # -------- FILTERS --------
    flavor = request.GET.get('flavor')
    price = request.GET.get('price')

    if flavor:
        puddings = puddings.filter(flavor=flavor)

    # -------- PRICE FILTER --------
    if price == '300-600':
        puddings = puddings.filter(price__gte=150, price__lte=450)
    elif price == '500-1000':
        puddings = puddings.filter(price__gte=500, price__lte=1000)
    elif price == '1000-1500':
        puddings = puddings.filter(price__gte=1000, price__lte=1500)
    elif price == 'low-high':
        puddings = puddings.order_by('price')
    elif price == 'high-low':
        puddings = puddings.order_by('-price')

    context = {
        'page_obj': puddings
    }

    return render(request, 'puddings.html', context)

def desserts(request):
    desserts = Dessert.objects.all()

    category = request.GET.get('category')
    flavor = request.GET.get('flavor')
    price = request.GET.get('price')

    # -------- CATEGORY FILTER --------
    if category:
        desserts = desserts.filter(category=category)

    # -------- FLAVOR FILTER --------
    if flavor:
        desserts = desserts.filter(flavor=flavor)

    # -------- PRICE FILTER --------
    if price == '150-450':
        desserts = desserts.filter(price__gte=150, price__lte=250)

    elif price == '500-1000':
        desserts = desserts.filter(price__gte=500, price__lte=1000)

    elif price == '1000-1500':
        desserts = desserts.filter(price__gte=1000, price__lte=1500)

    elif price == 'low-high':
        desserts = desserts.order_by('price')

    elif price == 'high-low':
        desserts = desserts.order_by('-price')

    # -------- PAGINATION --------
    paginator = Paginator(desserts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'desserts.html', {
        'page_obj': page_obj
    })

def sugarfree(request):
    return render(request,'sugarfree.html')

def gift(request):
    return render(request,'gift.html')


def search(request):
    query = request.GET.get('q')
    results = {}

    if query:
        queryset = ProductSearch.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(flavor__icontains=query)
        )

        # group by product type (for your UI sections)
        results = {
            'cakes': queryset.filter(product_type='cake'),
            'desserts': queryset.filter(product_type='dessert'),
            'puddings': queryset.filter(product_type='pudding'),
            'sugarfree': queryset.filter(product_type='sugarfree'),
            'gift': queryset.filter(product_type='gift'),
        }

    return render(request, 'search_results.html', {
        'query': query,
        'results': results
    })

def ajax_search(request):
    query = request.GET.get('q', '').strip()

    results = []

    if query:
        items = ProductSearch.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(flavor__icontains=query)
        )[:8]  # limit results (important)

        for item in items:
            results.append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'image': item.image.url,
                'type': item.product_type
            })

    return JsonResponse({'results': results})

def search_redirect(request, id):
    item = get_object_or_404(ProductSearch, id=id)

    if item.product_type == 'cake':
        return redirect('cake_detail', item.product_id)
    elif item.product_type == 'dessert':
        return redirect('dessert_detail', item.product_id)
    elif item.product_type == 'pudding':
        return redirect('pudding_detail', item.product_id)
    elif item.product_type == 'sugarfree':
        return redirect('sugarfree_detail', item.product_id)
    elif item.product_type == 'gift':
        return redirect('gift_detail', item.product_id)