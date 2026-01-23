from django.contrib import admin
from .models import Cake

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'flavor', 'structure')
    list_filter = ('category', 'flavor', 'structure')
    search_fields = ('name',)
