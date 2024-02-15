from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import os


class BotAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        print(1)
        if not token or token != os.environ.get('API_TOKEN'):
            raise AuthenticationFailed('Invalid Token')
        return (None, None)
