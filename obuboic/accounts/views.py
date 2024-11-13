import jwt
import random
import requests
from datetime import datetime, timedelta
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User, Member, AuthTable
from .serializers import KakaoSignUpSerializer, CheckPasswordSerializer, MemberSerializer, CheckNicknameSerializer, CheckUserIdSerializer, AuthTablePhoneSerializer, AuthTableSerializer, SignUpSerializer
from sms import message
from common import response
from .jwt_handler import decode_token, decode_token_without_exp
from .oauth import kakao

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')
SMS_API_KEY = getattr(settings, "SMS_API_KEY")
SMS_API_SECRET = getattr(settings, "SMS_API_SECRET")
KAKAO_CLIENT_ID = getattr(settings, "KAKAO_CLIENT_ID")
KAKAO_SIGNUP_REDIRECT_URI = getattr(settings, "KAKAO_SIGNUP_REDIRECT_URI")
KAKAO_LOGIN_REDIRECT_URI = getattr(settings, "KAKAO_LOGIN_REDIRECT_URI")
KAKAO_AUTH_GET_TOKEN_URI = getattr(settings, "KAKAO_AUTH_GET_TOKEN_URI")
KAKAO_AUTH_GET_USER_INFO = getattr(settings, "KAKAO_AUTH_GET_USER_INFO")


def auth_request(phone):
    # 인증코드 생성 및 저장
    code = str(random.randint(100000, 999999))
    AuthTable.objects.create(phone=phone, code=code)

    # 인증 코드 전송
    res_code = message.send_sms(SMS_API_KEY, SMS_API_SECRET, phone, code)

    return res_code


# -- 회원가입 -- #
class UserCreateView(APIView):
    # 중복 아이디 확인
    def get(self, request, username):
        try:
            query_dict = QueryDict('username='+username)
            serializer = CheckUserIdSerializer(data=query_dict)

            if serializer.is_valid(raise_exception=True):
                return response.HTTP_200

        except Exception as e:
            return response.http_400(str(e))

    # 회원가입
    def post(self, request):
        try:
            serializer = SignUpSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.HTTP_201

        except Exception as e:
            return response.http_400(str(e))


# 닉네임 중복 확인
class CheckNickname(APIView):
    def get(self, request, nickname):
        try:
            query_dict = QueryDict('nickname='+nickname)
            serializer = CheckNicknameSerializer(data=query_dict)

            if serializer.is_valid(raise_exception=True):
                return response.HTTP_200

        except Exception as e:
            return response.http_400(str(e))


# 계정 조회/수정 API
class UserProfileView(APIView):
    def get(self, request):
        access_token = request.headers.get('Authorization', None)  # 토큰 조회

        # 토큰 decoding
        try:
            payload = decode_token(access_token)  # 토큰 decoding
            user = get_object_or_404(User, pk=payload.get('user_id'))
        except Exception as e:
            return response.http_400(str(e))

        member = get_object_or_404(Member, user=user)
        member_serializer = MemberSerializer(instance=member)
        result = {"member": member_serializer.data}

        return response.http_200(result)

    def put(self, request):
        access_token = request.headers.get('Authorization', None)  # 토큰 조회

        # 토큰 decoding
        try:
            payload = decode_token(access_token)  # 토큰 decoding
            user = get_object_or_404(User, pk=payload.get('user_id'))
        except Exception as e:
            return response.http_400(str(e))

        serializer = MemberSerializer(data=request.data)            # 요청 데이터 직렬화

        if serializer.is_valid(raise_exception=True):               # 요청 데이터 유효성 검사
            member = get_object_or_404(Member, user=user)
            updated_member = serializer.update(member, serializer.validated_data)    # 회원 인스턴스 수정

            member_serializer = MemberSerializer(instance=updated_member)
            result = {"member": member_serializer.data}

            return response.http_200(result)


# 계정 로그인 API
class LoginView(APIView):
    def post(self, request):
        try:
            # ID/PW 인증
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))

            # 인증 통과시(회원이 존재하는 경우)
            if user is not None:
                # JWT 토큰 발급
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)

                # 해당 회원의 Refresh Token 저장
                user.refresh_token = refresh_token
                user.last_login = datetime.now()
                user.save()

                result = {"token": {"access": access_token, "refresh": refresh_token}}
                return response.http_200(result)
            else:
                return response.http_400("회원정보가 올바르지 않습니다.")

        except Exception as e:
            return response.http_400(str(e))


# 계정 로그아웃 API
class LogoutView(APIView):
    def post(self, request):
        refresh = request.headers.get('Authorization', None)

        # JWT 인증 - 기간만료 무시
        try:
            payload = decode_token_without_exp(refresh)
        except Exception as e:
            return response.http_400(str(e))

        # 사용자 조회
        user = get_object_or_404(User, pk=payload.get('user_id'))

        # 해당 회원의 Refresh Token 삭제
        user.refresh_token = None
        user.save()

        return response.HTTP_200


# 회원 탈퇴 API
class WithdrawalView(APIView):
    def post(self, request):
        access_token = request.headers.get('Authorization', None)  # 토큰 조회

        # 토큰 decoding
        try:
            payload = decode_token(access_token)  # 토큰 decoding
        except Exception as e:
            return response.http_400(str(e))

        user = get_object_or_404(User, pk=payload.get('user_id'))
        user.delete()

        return response.HTTP_200


# AccessToken 재발급 API
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        # 토큰 decoding
        try:
            payload = decode_token(refresh_token)  # 토큰 decoding
            user = get_object_or_404(User, pk=payload.get('user_id'))
        except Exception as e:
            return response.http_400(str(e))

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


# -- 인증번호 전송  -- #
class AuthSMS(APIView):
    def post(self, request):
        # 데이터 유효성 검사
        serializer = AuthTablePhoneSerializer(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data["phone"]

            res_code = auth_request(phone)

            if res_code == 200:
                return response.HTTP_200
            else:
                return response.http_503("인증문자 전송 실패")
        else:
            return response.http_400("전화번호를 확인해주세요.")


# -- 회원 아이디 인증 -- #
class AuthUserWithId(APIView):
    def get(self, request, username):
        user_exist = User.objects.filter(username=username).exists()

        if user_exist:
            return response.HTTP_200
        else:
            return response.http_404("ID를 확인해주세요.")

    def post(self, request):
        username = request.data['username']
        phone = request.data['phone']

        member = get_object_or_404(Member, phone=phone)
        db_username = member.user.username

        if username == db_username:
            res_code = auth_request(phone)

            if res_code == 200:
                return response.HTTP_200
            else:
                return response.http_503("인증문자 전송 실패")
        else:
            return response.http_401("회원가입 시 기입한 아이디를 입력해주세요.")


# -- 회원 이름 인증 -- #
class AuthUserWithName(APIView):
    def post(self, request):
        name = request.data['name']
        phone = request.data['phone']

        member = get_object_or_404(Member, phone=phone)

        if name == member.name:
            res_code = auth_request(phone)

            if res_code == 200:
                return response.HTTP_200
            else:
                return response.http_503("인증문자 전송 실패")
        else:
            return response.http_401("회원가입 시 기입한 이름을 입력해주세요.")


# -- 인증코드 확인 -- #
class AuthVerify(APIView):
    def post(self, request):
        phone = request.data["phone"]
        code = request.data["code"]

        # 현재 시간 체크
        current_time = datetime.now()

        # 인증 데이터 조회
        auth_instance = AuthTable.objects.filter(phone=phone).order_by('-created_at').first()

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


class UserPasswordView(APIView):
    # -- 비밀번호 확인 -- #
    def get(self, request):
        access_token = request.headers.get('Authorization', None)  # 토큰 조회
        password = request.data['password']

        # 토큰 decoding
        try:
            payload = decode_token(access_token)  # 토큰 decoding
            user = get_object_or_404(User, pk=payload.get('user_id'))

        except Exception as e:
            return response.http_400(str(e))

        if user.check_password(password):
            return response.HTTP_200
        else:
            return response.http_403("비밀번호가 일치하지 않습니다.")

    # -- 비밀번호 변경 -- #
    def put(self, request):
        try:
            access_token = request.headers.get('Authorization', None)   # 토큰 조회
            payload = decode_token(access_token)                        # 토큰 decoding
        except Exception as e:
            return response.http_400(str(e))

        user = get_object_or_404(User, pk=payload.get('user_id'))
        serializer = CheckPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data['password']

            user.set_password(new_password)
            user.save()

            return response.HTTP_200


class PasswordSetView(APIView):
    def put(self, request):
        username = request.data['username']
        user = get_object_or_404(User, username=username)

        new_password = request.data['password']
        serializer = CheckPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.set_password(new_password)
            user.save()

        return response.HTTP_200


# -- 아이디 찾기(부분) -- #
class FindUserPartId(APIView):
    def post(self, request):
        name = request.data['name']
        phone = request.data['phone']

        member = get_object_or_404(Member, phone=phone)

        if member.name == name:
            username = member.user.username[0:3]
            for i in range(len(username[3:])):
                username = username + "*"

            return response.http_200(username)
        else:
            return response.http_404("해당 회원이 존재하지 않습니다.")


# -- 아이디 찾기(전체) -- #
class FindId(APIView):
    def get(self, request):
        phone = request.data['phone']
        member = get_object_or_404(Member, phone=phone)
        result = response.make_result2("id", member.user.username, "date", member.user.created_at)

        return response.http_200(result)


class KakaoSignUp(APIView):
    def get(self, request):
        authorization_code = request.GET.get('code', None)
        return response.http_200(authorization_code)

    def post(self, request):
        try:
            authorization_code = request.data.get('code')               # 인가코드 조회
            access_token = kakao.get_access_token(authorization_code)   # 토큰 요청
            username = kakao.get_user_id(access_token)                  # 카카오 계정 코드
            name = kakao.get_user_nickname(access_token)                # 카카오 닉네임

            request_data = request.POST.copy()
            request_data['username'] = username
            request_data['password'] = username
            request_data['name'] = name

            serializer = KakaoSignUpSerializer(data=request_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return response.HTTP_200

        except Exception as e:
            return response.http_400(str(e))


class KakaoLogin(APIView):
    def post(self, request):
        authorization_code = request.data.get('code', None)           # 인가코드 추출
        access_token = kakao.get_access_token(authorization_code)     # 토큰 요청
        username = kakao.get_user_id(access_token)                    # 카카오 계정 코드

        user_exist = User.objects.filter(username=username).exists()
        user = get_object_or_404(User, username=username)

        if user_exist:
            # JWT 토큰 발급
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            # 해당 회원의 Refresh Token 저장
            user.refresh_token = refresh_token
            user.last_login = datetime.now()
            user.save()

            result = {"token": {"access": access_token, "refresh": refresh_token}}
            return response.http_200(result)
        else:
            return response.http_400("회원정보가 올바르지 않습니다.")


