from django.utils.deprecation import MiddlewareMixin
from jwt import decode, InvalidTokenError
from django.conf import settings

class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization', None)
        if auth_header is not None and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                request.user_info = {
                    'username': payload.get('username'),
                    'full_name': payload.get('full_name'),
                }
            except InvalidTokenError:
                pass