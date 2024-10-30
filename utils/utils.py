from datetime import datetime


def set_activity_expiry(request):
    user = request.user
    if not user.is_anonymous:
        user.last_active_datetime = datetime.now()
        user.save()
        request.session.set_expiry(60)
