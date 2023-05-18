from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from rest_framework import exceptions

class BearerTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    model = None

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        auth = auth_header.split(' ')
        if len(auth) != 2 or auth[0] != self.keyword:
            return None

        token = auth[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')

        user_data = payload.get('user_data')
        if not user_data:
            raise exceptions.AuthenticationFailed('Missing user data in token')

        return (None, user_data)
