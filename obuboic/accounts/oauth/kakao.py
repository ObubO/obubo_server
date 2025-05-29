import requests
from django.conf import settings

KAKAO_CLIENT_ID = getattr(settings, "KAKAO_CLIENT_ID")
KAKAO_LOGIN_CALLBACK_URI = getattr(settings, "KAKAO_LOGIN_CALLBACK_URI")
KAKAO_SIGNUP_CALLBACK_URI = getattr(settings, "KAKAO_SIGNUP_CALLBACK_URI")
KAKAO_REQUEST_TOKEN_URI = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code"
KAKAO_REQUEST_CODE_URI = "https://kauth.kakao.com/oauth/authorize?response_type=code"
KAKAO_302_REDIRECT_URI = "https://nursinghome.ai/kakao/signUp2"


# 인가코드 요청(로그인)
def request_auth():
    request_url = f'{KAKAO_REQUEST_CODE_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_LOGIN_CALLBACK_URI}'

    return request_url


# 토큰 요청(로그인)
def request_token(code):
    token_request = requests.post(
        f'{KAKAO_REQUEST_TOKEN_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_LOGIN_CALLBACK_URI}&code={code}'
    )

    kakao_token = token_request.json()

    return kakao_token


# 인가코드 요청(회원가입)
def request_auth_signup():
    request_url = f'{KAKAO_REQUEST_CODE_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_SIGNUP_CALLBACK_URI}'

    return request_url


# 토큰 요청(회원가입)
def request_token_signup(code):
    token_request = requests.post(
        f'{KAKAO_REQUEST_TOKEN_URI}&client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_SIGNUP_CALLBACK_URI}&code={code}'
    )

    kakao_token = token_request.json()

    return kakao_token


# 카카오 회원정보 조회
def get_accounts_info(token):
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {token}"}
    )

    accounts_info = profile_request.json()

    return accounts_info


# 카카오 회원번호 조회
def get_user_id(token):
    accounts_info = get_accounts_info(token)
    user_id = accounts_info.get('kakao_account')['email']

    if user_id is None:
        user_id = "K" + str(accounts_info.get("id"))

    return user_id


# 카카오 회원 닉네임 조회
def get_user_name(token):
    accounts_info = get_accounts_info(token)
    name = str(accounts_info.get("properties")["nickname"])

    return name


# 카카오 회원 프로필 조회
def get_user_profile(token):
    accounts_info = get_accounts_info(token)
    profile = accounts_info.get("kakao_account")

    return profile


def get_user_email(token):
    profile = get_user_profile(token)
    email = profile.get('email')

    return email
