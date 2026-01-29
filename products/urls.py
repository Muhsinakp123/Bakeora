from django.urls import path
from . import views

urlpatterns = [   
    path('cakes/',views.cakes,name='cakes'),
    path('puddings/',views.puddings,name='puddings'),
    path('desserts/',views.desserts,name='desserts'),
    
    path('shop/', views.shop, name='shop'),
    path('cake/<int:id>/', views.cake_detail, name='cake_detail'),
]