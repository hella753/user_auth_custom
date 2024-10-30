from datetime import datetime


def set_activity_expiry(request):
    """
    This function updates the last_active record to current datetime,
    saves it in the database and sets the expiry of the session to 1m.
    """
    user = request.user
    if not user.is_anonymous:
        user.last_active_datetime = datetime.now()
        user.save()
        request.session.set_expiry(60)
