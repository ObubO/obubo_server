import requests
from django.http import HttpResponseRedirect
from django.conf import settings

KAKAO_CLIENT_ID = getattr(settings, "KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = getattr(settings, "KAKAO_REDIRECT_URI")
KAKAO_REDIRECT_URI_SIGNUP = getattr(settings, "KAKAO_REDIRECT_URI_SIGNUP")
KAKAO_AUTH_TOKEN_URI = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code"
KAKAO_AUTH_CODE_URI = "https://kauth.kakao.com/oauth/authorize?response_type=code"


def request_auth():
    request_url = f'{KAKAO_AUTH_CODE_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}'

    return HttpResponseRedirect(request_url)


def request_auth_signup():
    request_url = f'{KAKAO_AUTH_CODE_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI_SIGNUP}'

    return HttpResponseRedirect(request_url)


def request_token(code):
    token_request = requests.post(
        f'{KAKAO_AUTH_TOKEN_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&code={code}'
    )

    kakao_token = token_request.json()

    return kakao_token


def request_token_signup(code):
    token_request = requests.post(
        f'{KAKAO_AUTH_TOKEN_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI_SIGNUP}&code={code}'
    )

    kakao_token = token_request.json()

    return kakao_token


def get_user_profiles(token):
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {token}"}
    )

    kakao_profile = profile_request.json()

    return kakao_profile


def get_user_id(token):
    profile = get_user_profiles(token)
    user_id = "K" + str(profile.get("id"))

    return user_id


def get_user_nickname(token):
    profile = get_user_profiles(token)
    name = str(profile.get("properties")["nickname"])

    return name
