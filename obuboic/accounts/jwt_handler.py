import jwt
from django.shortcuts import get_object_or_404
from django.conf import settings


SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')


def decode_token(token):
    try:
        # JWT 인증(Access Token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        return payload

    # Token has expired
    except jwt.exceptions.ExpiredSignatureError:
        raise Exception("expired_token")

    # Invalid token
    except jwt.exceptions.InvalidTokenError:
        raise Exception("invalid_token")
