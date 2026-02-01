from django.contrib import admin
from .models import Cake, Dessert, Pudding, ProductSearch

admin.site.register(Dessert)
admin.site.register(Pudding)
admin.site.register(ProductSearch)


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'flavor', 'structure')
    list_filter = ('category', 'flavor', 'structure')
    search_fields = ('name',)
