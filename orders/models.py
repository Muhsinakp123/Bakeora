from django.db import models
from django.conf import settings

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

    SIZE_CHOICES = [
        ('500g', '500g'),
        ('1kg', '1kg'),
        ('2kg', '2kg'),
        ('custom', 'Custom Size'),
    ]

    FLAVOR_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('vanilla', 'Vanilla'),
        ('red_velvet', 'Red Velvet'),
        ('custom', 'Custom Flavor'),
    ]

    CREAM_CHOICES = [
        ('buttercream', 'Buttercream'),
        ('whipped', 'Whipped Cream'),
        ('fondant', 'Fondant'),
        ('custom', 'Custom Cream'),
    ]

    # Structured selections
    cake_size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    flavor = models.CharField(max_length=30, choices=FLAVOR_CHOICES)
    cream_type = models.CharField(max_length=30, choices=CREAM_CHOICES)

    # Custom fields (only used if "custom" selected)
    custom_size = models.CharField(max_length=20, blank=True, null=True)
    custom_flavor = models.CharField(max_length=50, blank=True, null=True)
    custom_cream = models.CharField(max_length=50, blank=True, null=True)

    # Optional photo
    reference_photo = models.ImageField(upload_to='cake_photos/', blank=True, null=True)

    # Message
    message_on_cake = models.CharField(max_length=200)

    # Delivery
    delivery_datetime = models.DateTimeField()
    delivery_address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flavor} - {self.cake_size}"
