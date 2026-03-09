from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('orders/',views.orders_list,name='admin_orders'),
    path("products/",views.products_list,name="admin_products"),
]
