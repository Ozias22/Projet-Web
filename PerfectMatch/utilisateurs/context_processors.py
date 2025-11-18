from utilisateurs.models import Message, UserProfile

def navbar_notifications(request):
    if not request.user.is_authenticated:
        return {"notif_count": 0, "notif_messages": []}

    try:
        profile = request.user.userprofile
    except:
        return {"notif_count": 0, "notif_messages": []}

    # Messages non lus
    unread_messages = Message.objects.filter(
        receiver=profile,
        is_read=False
    ).order_by("-timestamp")[:3]  # on limite à 5

    return {
        "notif_count": unread_messages.count(),
        "notif_messages": unread_messages
    }
