from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from .models import CustomCakeOrder
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def custom_order(request):

    if request.method == "POST":
        order = CustomCakeOrder.objects.create(
            user=request.user,
            cake_type=request.POST['cake_type'],
            flavor=request.POST['flavor'],
            size=request.POST['size'],
            message_on_cake=request.POST.get('message'),
            delivery_date=request.POST['delivery_date'],
            notes=request.POST.get('notes')
        )

        return redirect('custom_checkout', order_id=order.id)

    return render(request, 'custom_order.html')

@login_required(login_url='login')
def custom_checkout(request, order_id):

    order = get_object_or_404(
        CustomCakeOrder,
        id=order_id,
        user=request.user
    )

    if request.method == "POST":
        # Later integrate Razorpay here
        order.status = 'paid'
        order.save()

        messages.success(request, "🎉 Order placed successfully!")
        return redirect('home')

    return render(request, 'custom_checkout.html', {
        'order': order
    })