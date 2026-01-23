from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)
