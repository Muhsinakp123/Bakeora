from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Orders
    path('orders/', views.all_orders, name='all_orders'),
    path('orders/pending/', views.pending_orders, name='pending_orders'),
    path('orders/preparing/', views.preparing_orders, name='preparing_orders'),
    path('orders/out-for-delivery/', views.out_for_delivery_orders, name='out_for_delivery_orders'),
    path('orders/delivered/', views.delivered_orders, name='delivered_orders'),
    path("orders/update-status/<int:order_id>/",views.update_order_status,name="update_order_status"),
    path('orders/<int:order_id>/',views.admin_order_detail,name='admin_order_detail'),
    
    path('custom-cakes/<int:cake_id>/',views.admin_custom_cake_detail,name='admin_custom_cake_detail'),
    path('custom-cakes/', views.custom_cakes_pending, name='custom_cakes_pending'),
    path('custom-cakes/quoted/', views.custom_cakes_quoted, name='custom_cakes_quoted'),
    path('custom-cakes/confirmed/', views.custom_cakes_confirmed, name='custom_cakes_confirmed'),
    path('custom-cakes/baking/', views.custom_cakes_baking, name='custom_cakes_baking'),
    path('custom-cakes/out-for-delivery/', views.custom_cakes_delivery, name='custom_cakes_delivery'),
    path('custom-cakes/delivered/', views.custom_cakes_delivered, name='custom_cakes_delivered'),

    # Products
    path("products/", views.products_list, name="admin_products"),
    
    path('customers/', views.customers_list, name='admin_customers'),
    path("subscribers/", views.subscribers_list, name="admin_subscribers"),
]