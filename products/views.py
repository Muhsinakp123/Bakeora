from django.shortcuts import render,get_object_or_404
from itertools import chain
import random
from .models import Cake,Dessert,Pudding
from django.core.paginator import Paginator
from products.models import ProductSearch

# Create your views here.


def cakes(request):
    cakes_qs = Cake.objects.all()

    category = request.GET.get('category')
    flavor = request.GET.get('flavor')
    structure = request.GET.get('structure')
    price = request.GET.get('price')

    if category and category != "all":
        cakes_qs = cakes_qs.filter(category=category)

    if flavor:
        cakes_qs = cakes_qs.filter(flavor=flavor)

    if structure:
        cakes_qs = cakes_qs.filter(structure=structure)

    if price == '400-1000':
        cakes_qs = cakes_qs.filter(price__range=(400,1000))
    elif price == '1000-2000':
        cakes_qs = cakes_qs.filter(price__range=(1000,2000))
    elif price == '2000-5000':
        cakes_qs = cakes_qs.filter(price__range=(2000,5000))
    elif price == 'low-high':
        cakes_qs = cakes_qs.order_by('price')
    elif price == 'high-low':
        cakes_qs = cakes_qs.order_by('-price')

    paginator = Paginator(cakes_qs, 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    # ✅ attach ProductSearch id
    for cake in page_obj:
        cake.ps = ProductSearch.objects.filter(
            product_type="cake",
            product_id=cake.id
        ).first()

    return render(request, "cakes.html", {
        "page_obj": page_obj,
        "categories": Cake._meta.get_field("category").choices,
        "flavors": Cake._meta.get_field("flavor").choices,
        "structures": Cake._meta.get_field("structure").choices,
    })


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
    
    for p in page_obj:
        p.ps = ProductSearch.objects.filter(
            product_type="pudding",
            product_id=p.id
            ).first()

    
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
    
    for d in page_obj:
        d.ps = ProductSearch.objects.filter(
            product_type="dessert",
            product_id=d.id
            ).first()

    return render(request, 'desserts.html', {
        'page_obj': page_obj
    })

def shop(request):

    selected_type = request.GET.get("type")
    selected_price = request.GET.get("price")

    cakes = Cake.objects.all()
    desserts = Dessert.objects.all()
    puddings = Pudding.objects.all()

    # ---------- TYPE FILTER ----------
    if selected_type == "cake":
        products = list(cakes)

    elif selected_type == "dessert":
        products = list(desserts)

    elif selected_type == "pudding":
        products = list(puddings)

    else:
        products = list(chain(cakes, desserts, puddings))
        random.shuffle(products)

    # ---------- PRICE FILTER ----------
    if selected_price == "under-500":
        products = [p for p in products if p.price < 500]

    elif selected_price == "500-1000":
        products = [p for p in products if 500 <= p.price <= 1000]

    elif selected_price == "low-high":
        products = sorted(products, key=lambda x: x.price)

    elif selected_price == "high-low":
        products = sorted(products, key=lambda x: x.price, reverse=True)

    # ---------- 🔥 ATTACH ProductSearch ----------
    for p in products:
        if isinstance(p, Cake):
            p.ps = ProductSearch.objects.filter(
                product_type="cake",
                product_id=p.id
            ).first()

        elif isinstance(p, Dessert):
            p.ps = ProductSearch.objects.filter(
                product_type="dessert",
                product_id=p.id
            ).first()

        elif isinstance(p, Pudding):
            p.ps = ProductSearch.objects.filter(
                product_type="pudding",
                product_id=p.id
            ).first()

    # ---------- PAGINATION ----------
    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "shop.html", {
        "page_obj": page_obj,
        "selected_type": selected_type,
        "selected_price": selected_price,
    })

def cake_detail(request, id):
    cake = get_object_or_404(Cake, id=id)

    ps = ProductSearch.objects.filter(
        product_type="cake",
        product_id=id
    ).first()

    return render(request, "cake_detail.html", {
        "cake": cake,
        "ps": ps
    })



def dessert_detail(request, id):
    dessert = get_object_or_404(Dessert, id=id)

    ps = ProductSearch.objects.filter(
        product_type="dessert",
        product_id=id
    ).first()

    return render(request, "dessert_detail.html", {
        "dessert": dessert,
        "ps": ps
    })

    
def pudding_detail(request, id):
    pudding = get_object_or_404(Pudding, id=id)

    ps = ProductSearch.objects.filter(
        product_type="pudding",
        product_id=id
    ).first()

    return render(request, "pudding_detail.html", {
        "pudding": pudding,
        "ps": ps
    })
