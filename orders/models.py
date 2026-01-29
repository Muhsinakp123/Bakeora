from django.db import models
from django.conf import settings
from products.models import ProductSearch

User = settings.AUTH_USER_MODEL


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    address_line = models.TextField()

    def __str__(self):
        return f"{self.city} - {self.pincode}"



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def get_total(self):
        return self.price * self.quantity


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

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='custom_cake'
    )

    cake_type = models.CharField(max_length=20, choices=CAKE_TYPE_CHOICES)
    flavor = models.CharField(max_length=20, choices=FLAVOR_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)

    message_on_cake = models.CharField(max_length=100, blank=True)
    delivery_date = models.DateField()
    notes = models.TextField(blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Custom Cake for Order #{self.order.id}"

