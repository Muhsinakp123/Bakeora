from django.contrib import admin
from .models import Order, OrderItem, CustomCake, Address


# ===================== ORDER ITEMS INLINE =====================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity")


# ===================== ORDER ADMIN =====================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username")
    ordering = ("-created_at",)

    inlines = [OrderItemInline]


# ===================== CUSTOM CAKE ADMIN =====================

@admin.register(CustomCake)
class CustomCakeAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "user",
        "cake_type",
        "price",
        "payment_status",
        "status",
        "created_at",
    )

    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("reference_number", "user__username")
    ordering = ("-created_at",)


# ===================== ADDRESS ADMIN =====================

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "city",
        "district",
        "state",
        "pincode",
        "created_at",
    )

    search_fields = ("user__username", "city", "district")
    ordering = ("-created_at",)