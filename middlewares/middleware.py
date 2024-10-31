from datetime import datetime
from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.time = datetime.now()
        user = request.user
        if not user.is_anonymous:
            user.last_active_datetime = request.time
            user.save()
            request.session.set_expiry(60)