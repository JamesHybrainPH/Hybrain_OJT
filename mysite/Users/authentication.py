import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class BearerTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        auth_header_parts = auth_header.split(' ')
        if len(auth_header_parts) != 2 or auth_header_parts[0] != self.keyword:
            return None

        token = auth_header_parts[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user_id = payload.get('user_id')
        user_data = payload.get('user_data')
        if not user_id or not user_data:
            raise AuthenticationFailed('Invalid token')

        return (user_data, None)