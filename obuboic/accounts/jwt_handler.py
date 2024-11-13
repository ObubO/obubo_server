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
        raise Exception("This token is expired")

    # Invalid token
    except jwt.exceptions.InvalidTokenError:
        raise Exception("invalid_token")


def decode_token_without_exp(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})

        return payload

    except jwt.exceptions.InvalidTokenError:
        raise Exception("invalid_token")
