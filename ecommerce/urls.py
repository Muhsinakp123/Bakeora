from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('cakes/',views.cakes,name='cakes'),
    path('puddings/',views.puddings,name='puddings'),
    path('desserts/',views.desserts,name='desserts'),
    path('dryfruits/',views.dryfruits,name='dryfruits'),
    path('sugarfree/',views.sugarfree,name='sugarfree'),
    path('gift/',views.gift,name='gift'),
]
