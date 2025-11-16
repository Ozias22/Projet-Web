from .models import Message
from utilisateurs.models import UserProfile

def navbar_notifications(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            unread = Message.objects.filter(receiver=profile, is_read=False).count()
        except:
            unread = 0
    else:
        unread = 0

    return {"notif_count": unread}

