import requests
from django.conf import settings

KAKAO_CLIENT_ID = getattr(settings, "KAKAO_CLIENT_ID")
KAKAO_SIGNUP_REDIRECT_URI = getattr(settings, "KAKAO_SIGNUP_REDIRECT_URI")
KAKAO_LOGIN_REDIRECT_URI = getattr(settings, "KAKAO_LOGIN_REDIRECT_URI")
KAKAO_AUTH_GET_TOKEN_URI = getattr(settings, "KAKAO_AUTH_GET_TOKEN_URI")
KAKAO_AUTH_REQUEST_CODE_URI = getattr(settings, "KAKAO_AUTH_REQUEST_CODE_URI")
KAKAO_AUTH_GET_USER_INFO = getattr(settings, "KAKAO_AUTH_GET_USER_INFO")


def request_auth_code():
    try:
        code_request = requests.get(
            f'{KAKAO_AUTH_REQUEST_CODE_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_SIGNUP_REDIRECT_URI}'
        )

    except Exception as e:
        raise Exception(e)

    return code_request


def get_auth_code(request):
    auth_code = request.GET.get('code', None)

    return auth_code


def get_access_token(code):
    try:
        # code는 카카오서버에서 발급한 인가코드
        token_request = requests.post(
            f'{KAKAO_AUTH_GET_TOKEN_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_SIGNUP_REDIRECT_URI}&code={code}'
        )
    except Exception as e:
        raise Exception(e)

    kakao_token = token_request.json()
    kakao_access_token = kakao_token.get("access_token")

    return kakao_access_token


def get_user_profiles(token):
    try:
        # token은 카카오서버에서 발급한 access_token
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {token}"}
        )
    except Exception as e:
        raise Exception(e)

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
