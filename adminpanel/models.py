from django.db import models
from orders.models import Order

# Create your models here.

class AdminProduct(models.Model):
    PRODUCT_TYPES = [
        ('cake', 'Cake'),
        ('dessert', 'Dessert'),
        ('pudding', 'Pudding'),
        ('gift', 'Gift'),
    ]

    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    base_price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.product_type})"

class ProductVariant(models.Model):
    product = models.ForeignKey(AdminProduct, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)  # 0.5kg / 1kg / Box
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)

class City(models.Model):
    name = models.CharField(max_length=100)

class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Pincode(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    delivery_charge = models.PositiveIntegerField()
    delivery_time_hours = models.IntegerField()

class ProductAvailability(models.Model):
    product = models.ForeignKey(AdminProduct, on_delete=models.CASCADE)
    pincode = models.ForeignKey(Pincode, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

class DeliveryPerson(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    active = models.BooleanField(default=True)

class DeliveryAssignment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(
        choices=[('percent', 'Percent'), ('flat', 'Flat')],
        max_length=10
    )
    value = models.PositiveIntegerField()
    min_order_value = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
