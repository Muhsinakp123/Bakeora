from django.urls import path
from . import views

urlpatterns = [
    path('custom-order/', views.custom_order, name='custom_order'),
    path('custom-checkout/<int:order_id>/', views.custom_checkout, name='custom_checkout'),
    path('checkout/', views.checkout, name='checkout'),

    path(
        'buy-now/<str:product_type>/<int:product_id>/',
        views.buy_now,
        name='buy_now'
    ),

    path(
        'buy-now/address/<str:product_type>/<int:product_id>/',
        views.buy_now_address,
        name='buy_now_address_with_product'
    ),

    path(
        'buy-now/create-order/<int:address_id>/<str:product_type>/<int:product_id>/',
        views.buy_now_create_order,
        name='buy_now_create_order'
    ),

    path('add-address/', views.add_address, name='add_address'),
    path('payment-page/', views.payment_page, name='payment_page'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path("proceed-payment/<int:address_id>/",views.proceed_payment,name="proceed_payment"),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
    path("my-orders/", views.my_orders, name="my_orders"),
    path("my-orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("custom-pay/<int:order_id>/", views.custom_pay_now, name="custom_pay_now"),
    
]

