from django.contrib import admin
from .models import ContactMessage, Subscriber,Notifications

# Register your models here.

admin.site.register(ContactMessage)
admin.site.register(Subscriber)
admin.site.register(Notifications)