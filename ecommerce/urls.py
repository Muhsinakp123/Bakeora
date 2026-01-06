from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('cakes/',views.cakes,name='cakes'),
    path('puddings/',views.puddings,name='puddings'),
    path('desserts/',views.desserts,name='desserts'),
    path('sugarfree/',views.sugarfree,name='sugarfree'),
    path('gift/',views.gift,name='gift'),
    
    path('search/', views.search, name='search'),
    path('ajax-search/', views.ajax_search, name='ajax_search'),
    path('search-redirect/<int:id>/', views.search_redirect, name='search_redirect'),
    
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),



]
