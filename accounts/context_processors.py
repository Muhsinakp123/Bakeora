from .models import Notifications

def notification_count(request):
    if request.user.is_authenticated:
        count = Notifications.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return {"unread_notifications_count": count}
    return {}