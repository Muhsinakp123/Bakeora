from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta

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

class CustomCake(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('quoted', 'Quoted'),
        ('confirmed', 'Confirmed'),
        ('baking', 'Baking'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    reference_number = models.CharField(max_length=20, unique=True, blank=True)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='custom_cakes',
        null=True,
        blank=True
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    cake_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    flavor = models.CharField(max_length=100)
    cream_type = models.CharField(max_length=100)

    message_on_cake = models.CharField(max_length=200, blank=True)
    reference_photo = models.ImageField(upload_to='cake_photos/', blank=True, null=True)

    delivery_datetime = models.DateTimeField()
    delivery_address = models.TextField()
    notes = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_ready_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference_number:
            year = timezone.now().year
            random_part = str(uuid.uuid4())[:4].upper()
            self.reference_number = f"BKOR-{year}-{random_part}"

        if self.status == "confirmed" and not self.estimated_ready_time:
            self.estimated_ready_time = timezone.now() + timedelta(hours=4)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference_number
