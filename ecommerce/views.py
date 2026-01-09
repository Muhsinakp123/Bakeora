from django.shortcuts import render, redirect, get_object_or_404 
from django.db.models import Q
from django.http import JsonResponse
from products.models import ProductSearch

# Create your views here.

def home(request):
    return render(request,'home.html')


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
    
    return redirect('home')  # Fallback for unknown product types

