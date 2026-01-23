from django.db import models
from django.conf import settings
from django.db import models
from django.conf import settings
from products.models import ProductSearch


# Create your models here.

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = [
    ('placed', 'Placed'),
    ('preparing', 'Preparing'),
    ('out_for_delivery', 'Out for Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
    ('refunded', 'Refunded'),
]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductSearch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    address_line = models.TextField()

    def __str__(self):
        return f"{self.city} - {self.pincode}"



class CustomCakeOrder(models.Model):

    CAKE_TYPE_CHOICES = [
        ('birthday', 'Birthday Cake'),
        ('wedding', 'Wedding Cake'),
        ('bento', 'Bento Cake'),
        ('kids', 'Kids Cake'),
        ('custom', 'Fully Custom'),
    ]

    FLAVOR_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('vanilla', 'Vanilla'),
        ('redvelvet', 'Red Velvet'),
        ('butterscotch', 'Butterscotch'),
        ('fruit', 'Fruit'),
    ]

    SIZE_CHOICES = [
        ('0.5kg', '0.5 Kg'),
        ('1kg', '1 Kg'),
        ('2kg', '2 Kg'),
        ('3kg', '3 Kg'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    cake_type = models.CharField(max_length=20, choices=CAKE_TYPE_CHOICES)
    flavor = models.CharField(max_length=20, choices=FLAVOR_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)

    message_on_cake = models.CharField(max_length=100, blank=True)
    delivery_date = models.DateField()
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.cake_type} ({self.size})"