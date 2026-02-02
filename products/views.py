from django.shortcuts import render,get_object_or_404
from .models import Cake,Dessert,Pudding
from django.core.paginator import Paginator
from products.models import ProductSearch

# Create your views here.

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

    # ---------- TAB FILTER (Warm / Chilled / Vegan) ----------
    type_filter = request.GET.get("type")
    if type_filter and type_filter != "all":
        puddings = puddings.filter(style=type_filter)

    # ---------- FLAVOR ----------
    flavor = request.GET.get("flavor")
    if flavor:
        puddings = puddings.filter(flavor=flavor)

    # ---------- PRICE ----------
    price = request.GET.get("price")

    if price == "150-450":
        puddings = puddings.filter(price__gte=150, price__lte=450)

    elif price == "450-800":
        puddings = puddings.filter(price__gte=450, price__lte=800)

    elif price == "low-high":
        puddings = puddings.order_by("price")

    elif price == "high-low":
        puddings = puddings.order_by("-price")

    # ---------- PAGINATION ----------
    paginator = Paginator(puddings, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "puddings.html", {
        "page_obj": page_obj
    })
    
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


def shop(request):
    products = ProductSearch.objects.all()

    product_type = request.GET.get('type')
    price = request.GET.get('price')

    if product_type:
        products = products.filter(product_type=product_type)

    if price == 'low-high':
        products = products.order_by('price')
    elif price == 'high-low':
        products = products.order_by('-price')
    elif price == 'under-500':
        products = products.filter(price__lte=500)
    elif price == '500-1000':
        products = products.filter(price__gte=500, price__lte=1000)

    context = {
        'products': products,
        'selected_type': product_type,
        'selected_price': price,
    }
    return render(request, 'shop.html', context)


def cake_detail(request, id):
    cake = get_object_or_404(Cake, id=id)

    # ensure product exists in ProductSearch
    product_search, created = ProductSearch.objects.get_or_create(
        product_id=cake.id,
        product_type='cake',
        defaults={
            'name': cake.name,
            'price': cake.price,
            'image': cake.image,
        }
    )

    return render(request, 'cake_detail.html', {
        'cake': cake,
        'product': product_search
    })
