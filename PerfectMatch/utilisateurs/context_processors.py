from utilisateurs.models import Message, UserProfile,Match

def navbar_notifications(request):
    if not request.user.is_authenticated:
        return {"notif_count": 0, "notif_messages": []}
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return {"notif_count": 0, "notif_messages": []}

    unread_messages = Message.objects.filter(
        receiver=profile,
        is_read=False
    ).order_by("-timestamp")[:5]

    match_not_mutial = Match.objects.filter(
        user2_id = profile,
        is_mutual = False
    )

    return {
        "notif_count": unread_messages.count() + match_not_mutial.count(),
        "notif_messages": unread_messages
    }
