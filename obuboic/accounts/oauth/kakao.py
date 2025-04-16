import requests
from django.http import HttpResponseRedirect
from django.conf import settings

KAKAO_CLIENT_ID = getattr(settings, "KAKAO_CLIENT_ID")
KAKAO_CALLBACK_URI = getattr(settings, "KAKAO_CALLBACK_URI")
KAKAO_CALLBACK_URI_SIGNUP = getattr(settings, "KAKAO_CALLBACK_URI_SIGNUP")
KAKAO_REQUEST_TOKEN_URI = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code"
KAKAO_REQUEST_CODE_URI = "https://kauth.kakao.com/oauth/authorize?response_type=code"
KAKAO_302_REDIRECT_URI = "https://nursinghome.ai/kakao/signUp2"


# 인가코드 요청(로그인)
def request_auth():
    request_url = f'{KAKAO_REQUEST_CODE_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_CALLBACK_URI}'

    return HttpResponseRedirect(request_url)


# 토큰 요청(로그인)
def request_token(code):
    token_request = requests.post(
        f'{KAKAO_REQUEST_TOKEN_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}'
    )

    kakao_token = token_request.json()

    return kakao_token


# 인가코드 요청(회원가입)
def request_auth_signup():
    request_url = f'{KAKAO_REQUEST_CODE_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_CALLBACK_URI_SIGNUP}'

    return HttpResponseRedirect(request_url)


# 토큰 요청(회원가입)
def request_token_signup(code):
    token_request = requests.post(
        f'{KAKAO_REQUEST_TOKEN_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_CALLBACK_URI_SIGNUP}&code={code}'
    )

    kakao_token = token_request.json()

    return kakao_token


# 카카오 회원 프로필 조회
def get_user_profiles(token):
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {token}"}
    )

    kakao_profile = profile_request.json()

    return kakao_profile


# 카카오 회원번호 조회
def get_user_id(token):
    profile = get_user_profiles(token)
    user_id = "K" + str(profile.get("id"))

    return user_id


# 카카오 회원 닉네임 조회
def get_user_nickname(token):
    profile = get_user_profiles(token)
    name = str(profile.get("properties")["nickname"])

    return name
