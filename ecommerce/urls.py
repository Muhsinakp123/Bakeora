from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),

    
    path('search/', views.search, name='search'),
    path('ajax-search/', views.ajax_search, name='ajax_search'),
    path('search-redirect/<int:id>/', views.search_redirect, name='search_redirect'),

]
