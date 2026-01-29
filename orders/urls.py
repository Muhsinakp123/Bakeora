from django.urls import path
from . import views

urlpatterns = [   
    path('custom-order/', views.custom_order, name='custom_order'),
    path('custom-checkout/<int:order_id>/', views.custom_checkout, name='custom_checkout'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy-now/<int:cake_id>/', views.buy_now, name='buy_now'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]
