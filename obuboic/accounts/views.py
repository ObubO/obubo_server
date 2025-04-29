import random
import string
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User, UserProfile, AuthTable
from .serializers import SignUpSerializer, KakaoSignUpSerializer, UserProfileSerializer, UserSerializer, \
    UserIdSerializer, NicknameSerializer, PhoneNumberValidateSerializer, AuthTableSerializer,  \
    UserWritePostSerializer, UserWriteCommentSerializer, UserLikePostSerializer, UserLikeCommentSerializer
from sms import coolsms
from common import response
from .oauth import kakao

from .authentication import JWTAuthentication

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')
SMS_API_KEY = getattr(settings, "SMS_API_KEY")
SMS_API_SECRET = getattr(settings, "SMS_API_SECRET")
PASSWORD_RESET_URL = "https://nursinghome.ai/user/password-reset"


def create_code():
    code = str(random.randint(100000, 999999))  # 인증코드 생성 및 저장
    return code


def check_is_exists_name_phone(name, phone):
    user_profile_exists = UserProfile.objects.filter(name=name, phone=phone).exists()
    if user_profile_exists:
        coolsms.send_sms_code(phone)
        return True
    else:
        return False


def check_is_exists_username_phone(username, phone):
    user_instance = get_object_or_404(User, username=username)
    if user_instance.user_profile.phone == phone:
        coolsms.send_sms_code(phone)
        return True
    else:
        return False


def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=length)) + random.choice('!@#$')
    return password


# -- 회원가입 -- #
class UserCreateView(APIView):
    # 중복 아이디 확인
    def get(self, request, username):
        serializer = UserIdSerializer(data={'username': username})
        if serializer.is_valid(raise_exception=True):
            return response.HTTP_200

    # 회원가입
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.HTTP_201


# 닉네임 중복 확인
class CheckNickname(APIView):
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
class LoginView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return response.http_400("아이디와 비밀번호를 입력해주세요.")

        user = authenticate(username=username, password=password)
        if user is None:
            return response.http_400("회원정보가 올바르지 않습니다.")

        token = TokenObtainPairSerializer.get_token(user)   # JWT 토큰 발급
        access_token = str(token.access_token)
        refresh_token = str(token)

        user.refresh_token = refresh_token          # refresh token 업데이트
        user.last_login = datetime.now()            # 마지막 로그인 시각 업데이트
        user.save(update_fields=["refresh_token", "last_login"])

        result = {"token": {"access": access_token, "refresh": refresh_token}}

        return response.http_200(result)


# 계정 로그아웃 API
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        user.refresh_token = None
        user.save(update_fields=["refresh_token"])

        return response.HTTP_200


# 회원 탈퇴 API
class WithdrawalView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        user.delete()

        return response.HTTP_200


# AccessToken 재발급 API
class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        refresh_token = request.headers.get('Authorization', None)  # 토큰 조회
        user = request.user

        # -- 탈취당한 Refresh Token 여부 -- #
        # 정상적 요청인 경우
        if refresh_token == user.refresh_token:
            data = {'refresh': refresh_token}
            token_serializer = TokenRefreshSerializer(data=data)

            if token_serializer.is_valid():
                access_token = token_serializer.validated_data
                result = {"token": access_token}
                return response.http_200(result)
            else:
                return response.http_503("서버 에러 발생")

        # 공격시도 감지
        else:
            return response.http_403("사용자가 삭제한 토큰입니다.")


# -- 아이디 찾기 -- #
class FindUsernameView(APIView):
    def post(self, request):
        name = request.data['name']
        phone = request.data['phone']

        user_profile = get_object_or_404(UserProfile, name=name, phone=phone)
        user = user_profile.user

        result = {"id": user.username, "date": user.created_at}

        return response.http_200(result)


# -- 비밀번호 확인 -- #
class PasswordConfirmView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        password = request.data['password']

        if user.check_password(password):
            return response.HTTP_200
        else:
            return response.HTTP_400


# -- 비밀번호 재설정 요청-- #
class PasswordResetRequestView(APIView):
    def post(self, request):
        phone = request.data['phone']
        user_profile = get_object_or_404(UserProfile, phone=phone)
        if not user_profile:
            return response.http_400("해당 전화번호로 가입한 사용자가 없습니다.")

        user = user_profile.user

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{PASSWORD_RESET_URL}/{uid}/{token}"
        coolsms.send_sms_link(SMS_API_KEY, SMS_API_SECRET, phone, reset_link)

        return response.http_200(reset_link)


# -- 비밀번호 재설정 -- #
class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        password = request.data.get("password")
        if not password:
            return response.http_400("새 비밀번호를 입력해주세요.")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (ValueError, TypeError):
            return response.http_400("잘못된 요청입니다.")

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return response.http_400("유효하지 않은 토큰입니다.")

        user.set_password(password)
        user.save()

        return response.http_200("비밀번호가 성공적으로 변경되었습니다.")


# -- 전화번호 인증  -- #
class PhoneVerificationView(APIView):
    def post(self, request):
        phone = request.data['phone']
        code = create_code()

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
            coolsms.send_sms_code(phone)
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


class KakaoAuth(APIView):
    def get(self, request):
        result = kakao.request_auth()

        return result


class KakaoCallback(APIView):
    def handle_kakao_login(self, user):
        # JWT 토큰 발급
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        # 해당 회원의 Refresh Token 저장
        user.refresh_token = refresh_token
        user.last_login = datetime.now()
        user.save()

        result = {"token": {"access": access_token, "refresh": refresh_token}}
        return result

    def get(self, request):
        authorization_code = request.GET.get('code', None)

        kakao_token = kakao.request_token(authorization_code)  # 토큰 요청
        access_token = kakao_token.get("access_token")

        username = kakao.get_user_id(access_token)

        user_exist = User.objects.filter(username=username).exists()

        if user_exist:
            user = get_object_or_404(User, username=username)
            result = self.handle_kakao_login(user)

            return response.http_200(result)
        else:
            # 카카오싱크 도입 이후 회원가입 진행
            return response.HTTP_400


class KakaoSignUp(APIView):
    def get(self, request):
        result = kakao.request_auth_signup()

        return result

    def post(self, request):
        try:
            authorization_code = request.data.get('code')               # 인가코드 조회

            kakao_token = kakao.request_token_signup(authorization_code)   # 토큰 요청
            access_token = kakao_token.get("access_token")

            request_data = request.POST.copy()
            request_data['username'] = kakao.get_user_id(access_token)  # 카카오 계정 코드
            request_data['name'] = kakao.get_user_nickname(access_token)                # 카카오 닉네임
            request_data['password'] = generate_password()

            serializer = KakaoSignUpSerializer(data=request_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return response.HTTP_200

        except Exception as e:
            return response.http_400(str(e))


class KakaoCallbackSignup(APIView):
    def get(self, request):
        authorization_code = request.GET.get('code', None)

        redirect_uri = f'{kakao.KAKAO_302_REDIRECT_URI}?code={authorization_code}'

        return HttpResponseRedirect(redirect_uri)


class UserWritePost(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserWritePostSerializer(instance=user)

        return response.http_200(serializer.data)


class UserWriteComment(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserWriteCommentSerializer(instance=user)

        return response.http_200(serializer.data)


class UserLikePost(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserLikePostSerializer(instance=user)

        return response.http_200(serializer.data)


class UserLikeComment(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserLikeCommentSerializer(instance=user)

        return response.http_200(serializer.data)

