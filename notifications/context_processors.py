from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    else:
        count = 0
        recent_notifications = []
    return {
        'notifications': count,
        'recent_notifications': recent_notifications
    }
