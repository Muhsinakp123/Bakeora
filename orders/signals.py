from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomCake
from accounts.models import Notifications

@receiver(pre_save, sender=CustomCake)
def order_status_change_email(sender, instance, **kwargs):
    if not instance.pk:
        return  # New order, no previous status

    try:
        old_order = CustomCake.objects.get(pk=instance.pk)
    except CustomCake.DoesNotExist:
        return

    if old_order.status != instance.status:
        subject = f"Your Bakeora Order {instance.reference_number} Status Updated"

        message = f"""
Hello {instance.user.username},

Your custom cake order status has been updated.

Order ID: {instance.reference_number}
New Status: {instance.get_status_display()}

Thank you for choosing Bakeora 
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )
        Notifications.objects.create(
            user=instance.user,
            title="Order Status Updated",
            message=f"Your order status changed to {instance.status}"
)