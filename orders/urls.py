from django.urls import path
from . import views

urlpatterns = [   
    path('custom-order/', views.custom_order, name='custom_order'),
    path('custom-checkout/<int:order_id>/', views.custom_checkout, name='custom_checkout'),
]