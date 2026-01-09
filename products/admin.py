from django.contrib import admin
from .models import Cake

# Register your models here.

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'flavor','structure')
