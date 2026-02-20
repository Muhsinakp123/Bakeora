from django.contrib import admin
from .models import CustomCake
# Register your models here.

@admin.register(CustomCake)
class CustomCakeOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'user',
        'cake_type',
        'price',
        'status',
        'created_at'
    )

    list_filter = ('status',)
    search_fields = ('order_id', 'user__username')