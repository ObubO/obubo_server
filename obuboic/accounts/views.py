import random
import string
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenVerifySerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User, UserProfile, AuthTable
from .serializers import SignUpSerializer, KakaoSignUpSerializer, UserProfileSerializer, UserSerializer, \
    UserIdSerializer, NicknameSerializer, PhoneNumberValidateSerializer, AuthTableSerializer,  \
    UserWritePostSerializer, UserWriteCommentSerializer, UserLikePostSerializer, UserLikeCommentSerializer, \
    CustomTokenObtainPairSerializer
from sms import coolsms
from common import response, functions
from .oauth import kakao

from .authentication import JWTAuthentication

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.contrib.auth.models import update_last_login

from django.core.cache import cache

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')
SMS_API_KEY = getattr(settings, "SMS_API_KEY")
SMS_API_SECRET = getattr(settings, "SMS_API_SECRET")


def generate_code():
    code = str(random.randint(100000, 999999))  # 인증코드 생성 및 저장
    return code


def generate_password(length=16):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=length)) + random.choice('!@#$')

    return password


def generate_nickname():
    while True:
        nickname = functions.create_nickname()
        if not UserProfile.objects.filter(nickname=nickname).exists():
            break

    return nickname


def logout(refresh_token):
    cache.delete(refresh_token)


# -- 회원가입 -- #
class UserSignupView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except Exception as e:
                return response.http_400(str(e))

            return response.HTTP_201


class UserIdCheckView(APIView):
    def get(self, request, username):
        serializer = UserIdSerializer(data={'username': username})
        if serializer.is_valid(raise_exception=True):
            return response.HTTP_200


class UserNicknameCheckView(APIView):
    def get(self, request, nickname):
        serializer = NicknameSerializer(data={'nickname': nickname})
        if serializer.is_valid(raise_exception=True):
            return response.HTTP_200


# 계정 조회/수정 API
class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user

        user_profile_instance = get_object_or_404(UserProfile, user=user)
        user_profile_serializer = UserProfileSerializer(instance=user_profile_instance)

        result = {"user_profile": user_profile_serializer.data}

        return response.http_200(result)

    def patch(self, request):
        user = request.user
        user_profile_instance = get_object_or_404(UserProfile, user=user)       # 회원 프로필 인스턴스 조회

        user_profile_serializer = UserProfileSerializer(data=request.data)      # 데이터 유효성 검사

        if user_profile_serializer.is_valid(raise_exception=True):
            updated_user_profile = user_profile_serializer.update(user_profile_instance, user_profile_serializer.validated_data)    # 회원 프로필 인스턴스 수정

            user_profile_serializer = UserProfileSerializer(instance=updated_user_profile)
            result = {"user_profile": user_profile_serializer.data}

            return response.http_200(result)


# 계정 로그인 API
class UserLoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return response.http_400("아이디/비밀번호를 입력해주세요.")

        user = authenticate(username=username, password=password)
        if user is None:
            return response.http_400("회원정보가 올바르지 않습니다.")

        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data

            update_last_login(None, user)
            cache.set(token['refresh'], user.username, 60*60*24)        #

            return response.http_200({"token": token})


# 계정 로그아웃 API
class UserLogoutView(APIView):
    def post(self, request):
        refresh = request.data.get('refresh')
        logout(refresh)
        return response.http_200("로그아웃 되었습니다.")


# 회원 탈퇴 API
class UserWithdrawalView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        user.delete()

        return response.HTTP_200


# AccessToken 재발급 API
class UserTokenRefreshView(TokenRefreshView):
    def post(self, request, **kwargs):
        refresh = request.data.get('refresh')
        token_info = {"token": refresh}

        try:
            TokenVerifySerializer(data=token_info).is_valid(raise_exception=True)
        except Exception:
            logout(refresh)
            return response.http_401("유효하지 않은 토큰입니다.")

        username = cache.get(refresh)
        if username is None:
            # logging & send message/mail
            # redis reset
            return response.http_403("탈취된 토큰일 가능성이 있습니다.")

        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data
            return response.http_200({"token": token})
        else:
            logout(refresh)
            return response.http_503("토큰을 재발급 할 수 없습니다.")


# -- 아이디 찾기 -- #
class UserFindIdView(APIView):
    def post(self, request):
        phone = request.data['phone']

        user_profile = get_object_or_404(UserProfile, phone=phone)
        user = user_profile.user

        result = {"id": user.username, "date": user.created_at}

        return response.http_200(result)


# -- 비밀번호 확인 -- #
class UserPasswordConfirmView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        password = request.data['password']

        if user.check_password(password):
            return response.HTTP_200
        else:
            return response.HTTP_400


class UserPasswordResetView(APIView):
    def post(self, request):
        username, password = request.data['username'], request.data['password']

        user = get_object_or_404(User, username=username)
        user.set_password(password)

        return response.HTTP_200


# -- 전화번호 인증  -- #
class PhoneVerificationView(APIView):
    def post(self, request):
        phone = request.data['phone']
        code = generate_code()

        serializer = PhoneNumberValidateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            AuthTable.objects.create(phone=phone, code=code)

        coolsms.send_sms_code(SMS_API_KEY, SMS_API_SECRET, phone, code)  # 인증 코드 전송

        return response.http_200('인증번호를 전송하였습니다.')


# -- 본인 인증 -- #
class NamePhoneVerificationView(APIView):
    def post(self, request):
        name, phone = request.data['name'], request.data['phone']

        if UserProfile.objects.filter(name=name, phone=phone).exists():
            code = generate_code()
            AuthTable.objects.create(phone=phone, code=code)
            coolsms.send_sms_code(SMS_API_KEY, SMS_API_SECRET, phone, code)  # 인증 코드 전송

            return response.HTTP_200
        else:
            return response.http_400('회원이 존재하지 않습니다.')


class IdPhoneVerificationView(APIView):
    def post(self, request):
        username, phone = request.data['username'], request.data['phone']

        if UserProfile.objects.filter(user__username=username, phone=phone).exists():
            code = generate_code()
            AuthTable.objects.create(phone=phone, code=code)
            coolsms.send_sms_code(SMS_API_KEY, SMS_API_SECRET, phone, code)  # 인증 코드 전송

            return response.HTTP_200
        else:
            return response.http_400('회원이 존재하지 않습니다.')


# -- 인증번호 확인 -- #
class VerificationCodeConfirmView(APIView):
    def post(self, request):
        phone, code = request.data["phone"], request.data["code"]
        current_time = datetime.now()
        auth_instance = AuthTable.objects.filter(phone=phone).order_by('-created_at').first()   # 인증 데이터 조회
        if auth_instance is None:
            return response.http_404("전화번호가 존재하지 않습니다.")

        serializer = AuthTableSerializer(instance=auth_instance)
        db_code = serializer.data['code']
        db_time = datetime.strptime(serializer.data['created_at'], "%Y-%m-%dT%H:%M:%S.%f")

        # 인증번호 유효성 검사
        time_difference = current_time - db_time
        if code == db_code:
            if time_difference <= timedelta(minutes=5):
                return response.HTTP_200
            else:
                return response.http_401("인증번호 유효기간이 만료되었습니다.")
        else:
            return response.http_400("인증번호를 확인해주세요.")


class KakaoLogin(APIView):
    def handle_kakao_login(self, user):
        token = CustomTokenObtainPairSerializer.generate_tokens_for_user(user)  # 토큰 발급
        update_last_login(None, user)  # 마지막 로그인 업데이트
        user.update_refresh_token(token['refresh'])  # refresh 업데이트

        return token

    def get(self, request):
        result = kakao.request_auth()           # 인가코드 요청

        return HttpResponseRedirect(result)

    def post(self, request):
        authorization_code = request.data.get('code', None)     # 인가코드 조회

        if authorization_code is None:
            return response.http_400("인가코드 조회 에러")

        kakao_token = kakao.request_token(authorization_code)  # 토큰 요청
        access_token = kakao_token.get("access_token")

        if access_token is None:
            error_message = kakao_token
            return response.http_400(error_message)

        username = kakao.get_user_id(access_token)
        user_exist = User.objects.filter(username=username).exists()

        if user_exist:
            user = get_object_or_404(User, username=username)   # User 인스턴스 조회
            token = self.handle_kakao_login(user)               # 로그인 토큰 생성

            return response.http_200({"token": token})
        else:
            # 카카오싱크 도입 이후 회원가입 진행
            return response.http_400('회원가입을 진행해주세요.')


class KakaoCallbackLogin(APIView):
    def get(self, request):
        authorization_code = request.GET.get('code', None)

        redirect_uri = f'{kakao.KAKAO_LOGIN_302_REDIRECT_URI}?code={authorization_code}'

        return HttpResponseRedirect(redirect_uri)


class KakaoSignUp(APIView):
    def get(self, request):
        result = kakao.request_auth_signup()

        return HttpResponseRedirect(result)

    def post(self, request):
        authorization_code = request.data.get('code')               # 인가코드 조회

        if authorization_code is None:
            return response.http_400("인가코드 조회 에러")

        kakao_token = kakao.request_token_signup(authorization_code)   # 토큰 요청
        access_token = kakao_token.get("access_token")

        if access_token is None:
            error_message = kakao_token
            return response.http_400(error_message)

        request_data = request.data.copy()
        request_data['username'] = kakao.get_user_id(access_token)      # 카카오 계정 코드
        request_data['password'] = generate_password()
        request_data['name'] = kakao.get_user_name(access_token)           # 카카오 닉네임
        request_data['nickname'] = generate_nickname()

        serializer = KakaoSignUpSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except Exception as e:
                return response.http_400(str(e))

            return response.HTTP_200


class KakaoCallbackSignup(APIView):
    def get(self, request):
        authorization_code = request.GET.get('code', None)

        redirect_uri = f'{kakao.KAKAO_SIGNUP_302_REDIRECT_URI}?code={authorization_code}'

        return HttpResponseRedirect(redirect_uri)


class UserWritePostView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserWritePostSerializer(instance=user)

        return response.http_200(serializer.data)


class UserWriteCommentView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserWriteCommentSerializer(instance=user)

        return response.http_200(serializer.data)


class UserLikePostView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserLikePostSerializer(instance=user)

        return response.http_200(serializer.data)


class UserLikeCommentView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserLikeCommentSerializer(instance=user)

        return response.http_200(serializer.data)

