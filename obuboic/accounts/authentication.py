from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt
from . models import User


SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')

        if not token:
            return None

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('토큰이 만료되었습니다.')

        except jwt.exceptions.InvalidTokenError:
            raise exceptions.AuthenticationFailed('유효하지 않은 토큰입니다.')

        user = get_object_or_404(User, pk=payload.get('user_id'))

        return user, None
