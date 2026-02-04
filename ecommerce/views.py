from django.shortcuts import render, redirect, get_object_or_404 
from django.db.models import Q
from django.http import JsonResponse
from products.models import ProductSearch,Cake,Pudding,Dessert
from accounts.models import ContactMessage
from rapidfuzz import fuzz
from .search_utils import normalize_query

# Create your views here.

def home(request):
    if request.method == "POST" and request.POST.get("form_type") == "contact":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )

    return render(request, "home.html")

def search(request):
    raw_query = request.GET.get("q", "")
    query = normalize_query(raw_query)

    base_qs = ProductSearch.objects.filter(is_active=True)

    # Broad DB filter first (fast pre-filter)
    db_matches = base_qs.filter(
        Q(name__icontains=query) |
        Q(category__icontains=query) |
        Q(flavor__icontains=query) |
        Q(tags__icontains=query)
    )

    scored = []

    for item in db_matches:
        score = 0

        score += fuzz.partial_ratio(query, item.name.lower()) * 3
        score += fuzz.partial_ratio(query, item.category.lower()) * 2
        score += fuzz.partial_ratio(query, item.flavor.lower()) * 2
        score += fuzz.partial_ratio(query, item.tags.lower())

        if score > 120:   # threshold
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])

    results = [x[1] for x in scored]

    context = {
        "query": raw_query,
        "results": results
    }

    return render(request, "search_results.html", context)


def ajax_search(request):
    q = request.GET.get("q", "").strip()

    if len(q) < 1:
        return JsonResponse([], safe=False)

    cakes = Cake.objects.filter(
        Q(name__icontains=q) | Q(flavor__icontains=q)
    )[:5]

    desserts = Dessert.objects.filter(
        Q(name__icontains=q) | Q(flavor__icontains=q)
    )[:5]

    puddings = Pudding.objects.filter(
        Q(name__icontains=q) | Q(flavor__icontains=q)
    )[:5]

    results = []

    for c in cakes:
        results.append({
            "name": c.name,
            "price": c.price,
            "image": c.image.url if c.image else "",
            "url": f"/cakes/{c.id}/"
        })

    for d in desserts:
        results.append({
            "name": d.name,
            "price": d.price,
            "image": d.image.url if d.image else "",
            "url": f"/desserts/{d.id}/"
        })

    for p in puddings:
        results.append({
            "name": p.name,
            "price": p.price,
            "image": p.image.url if p.image else "",
            "url": f"/puddings/{p.id}/"
        })

    return JsonResponse(results, safe=False)


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
    
    return redirect('home')  # Fallback for unknown product types

