from django.utils.deprecation import MiddlewareMixin

from apps.users.models.user import CustomAnonymousUser


class CustomAnonymousUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated:
            request.user = CustomAnonymousUser()
