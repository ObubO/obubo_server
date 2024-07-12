import jwt
import random
from datetime import datetime, timedelta
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User, UserType, Member, TAC, TACAgree, AuthTable
from .serializers import UserSerializer, UserPasswordSerializer, MemberSerializer, CheckMemberNameSerializer, CheckUserIdSerializer, AuthTablePhoneSerializer, AuthTableSerializer
from sms import message
from common import response

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')
SMS_API_KEY = getattr(settings, "SMS_API_KEY")
SMS_API_SECRET = getattr(settings, "SMS_API_SECRET")

TACS = [[1, 'tac1'], [2, 'tac2'], [3, 'tac3'], [4, 'tac4']]


def home(request):
    return render(request, 'index.html')


# -- 회원가입 -- #

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(APIView):
    # 중복 아이디 확인
    def get(self, request, username):
        query_dict = QueryDict('username='+username)
        serializer = CheckUserIdSerializer(data=query_dict)

        if serializer.is_valid():
            return response.HTTP_200
        else:
            return response.http_400(serializer.errors)

    # 회원가입
    def post(self, request):
        member_serializer = MemberSerializer(data=request.data)
        user_serializer = UserSerializer(data=request.data)

        # 회원관리(User) 인스턴스 생성
        if user_serializer.is_valid():
            username = user_serializer.validated_data["username"]   # 회원 구분 key

            User.objects.create_user(
                username=username,
                password=user_serializer.validated_data["password"],
            )

            user = get_object_or_404(User, username=username)

        else:
            return response.http_400(user_serializer.errors)

        # 회원정보(Member) 인스턴스 선언
        if member_serializer.is_valid():
            member = Member(
                user=user,
                name=member_serializer.validated_data["name"],
                gender=member_serializer.validated_data["gender"],
                birth=member_serializer.validated_data["birth"],
                phone=member_serializer.validated_data["phone"],
                email=member_serializer.validated_data["email"],
                user_type=get_object_or_404(UserType, id=request.data.get("typeNo")),
            )

        else:
            User.objects.filter(username=username).delete()
            return response.http_400(member_serializer.errors)

        # 약관동의 인스턴스 생성
        try:
            for tac in TACS:
                tac_no, is_consent = tac[0], tac[1]
                TACAgree.objects.create(
                    user=user,
                    tac=get_object_or_404(TAC, id=tac_no),
                    is_consent=request.data[is_consent],
                    consent_date=datetime.now(),
                )
            member.save()

            return response.HTTP_201

        except:
            User.objects.filter(username=username).delete()
            return response.http_400("약관동의는 필수항목입니다")


class CheckMemberName(APIView):
    # 중복 아이디 확인
    def get(self, request, name):
        query_dict = QueryDict('name='+name)
        serializer = CheckMemberNameSerializer(data=query_dict)

        if serializer.is_valid():
            return response.HTTP_200
        else:
            return response.http_400(serializer.errors)


# 계정 조회/수정 API
class AuthView(APIView):
    def get(self, request):
        try:
            access = request.headers.get('Authorization', None)

            # JWT 인증(Access Token)
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

            # 사용자 조회
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            member = get_object_or_404(Member, user=user)
            serializer = MemberSerializer(instance=member)

            result = {"user": serializer.data}

            return response.http_200(result)

            # Access_Token 기간 만료
        except jwt.exceptions.ExpiredSignatureError:
            return response.http_401("토큰의 기간이 만료되었습니다.")

            # 사용 불가능 토큰
        except jwt.exceptions.InvalidTokenError:
            return response.http_400("사용할 수 없는 토큰입니다.")


# 계정 로그인 API
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        try:
            # ID/PW 인증
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
            is_active = user.is_active
            # 인증 통과시(회원이 존재하는 경우)
            if user is not None and is_active:
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

        except:
            return response.http_400("회원정보를 확인해주세요.")


# 계정 로그아웃 API
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        refresh = request.headers.get('Authorization', None)
        try:
            # JWT 인증(Refesh Token) - 기간만료 무시
            payload = jwt.decode(refresh, SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})

            # 사용자 조회
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            # 해당 회원의 Refresh Token 삭제
            user.refresh_token = None
            user.save()

            return response.HTTP_200

        except jwt.exceptions.InvalidTokenError:
            return response.http_400("유효하지 않은 토큰입니다.")


# 회원 탈퇴 API
class WithdrawalView(APIView):
    def post(self, request):
        try:
            access = request.headers.get('Authorization', None)

            # JWT 인증(Access Token)
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

            # 사용자 조회
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            user.is_active = False
            user.save()

            return response.HTTP_200

            # Access_Token 기간 만료
        except jwt.exceptions.ExpiredSignatureError:
            return response.http_401("토큰의 기간이 만료되었습니다.")

            # 사용 불가능 토큰
        except jwt.exceptions.InvalidTokenError:
            return response.http_400("사용할 수 없는 토큰입니다.")


# AccessToken 재발급 API
@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            # JWT 인증(Refresh Token)
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])

            # 사용자 조회
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)

        # -- 탈취당한 Refresh Token 여부 -- #
            # 정상적 요청인 경우
            if refresh_token == serializer.data.get('refresh_token'):
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

        # 기간 만료된 토큰
        except jwt.exceptions.ExpiredSignatureError:
            return response.http_401("토큰의 기간이 만료되었습니다.")

        # 사용 불가능 토큰
        except jwt.exceptions.InvalidTokenError:
            return response.http_400("사용할 수 없는 토큰입니다.")


# -- 전화번호 인증코드 요청 -- #
class AuthRequest(APIView):
    def post(self, request):
        # 데이터 유효성 검사
        serializer = AuthTablePhoneSerializer(data=request.data)

        # 인증 정보 저장
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            code = str(random.randint(100000, 999999))

            AuthTable.objects.create(phone=phone, code=code)

            # 인증 코드 전송
            # res_code = message.send_sms(SMS_API_KEY, SMS_API_SECRET, phone, code)
            res_code = 200
            if res_code == 200:
                return response.HTTP_200
            else:
                return response.http_503("인증문자 전송 실패")
        else:
            return response.http_400("전화번호를 확인해주세요.")


# -- 회원 인증코드 요청 -- #
class AuthUserRequest(APIView):
    def get(self, request, username):
        user_exist = User.objects.filter(username=username).exists()

        if user_exist:
            return response.HTTP_200
        else:
            return response.http_404("ID를 확인해주세요.")

    def post(self, request):
        username = request.data['username']
        phone = request.data['phone']

        # 회원 조회
        user = get_object_or_404(User, username=username)
        member = get_object_or_404(Member, user=user)
        db_serializer = MemberSerializer(instance=member)
        db_phone = db_serializer.data['phone']

        if phone == db_phone:
            # 인증코드 발급
            code = str(random.randint(100000, 999999))
            AuthTable.objects.create(phone=phone, code=code)

            # 인증코드 전송
            # res_code = message.send_sms(SMS_API_KEY, SMS_API_SECRET, phone, code)
            res_code = 200
            if res_code == 200:
                return response.HTTP_200
            else:
                return response.http_503("인증문자 전송 실패.")
        else:
            return response.http_401("회원가입 시 기입한 비밀번호를 입력해주세요.")


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
            if time_difference <= timedelta(minutes=3):
                return response.HTTP_200
            else:
                return response.http_401("인증번호 유효기간이 만료되었습니다.")
        else:
            return response.http_400("인증번호를 확인해주세요.")


# -- 비밀번호 변경 -- #
class ChangePassword(APIView):
    def post(self, request):
        serializer = UserPasswordSerializer(data=request.data)
        username = request.data['username']

        if serializer.is_valid():
            password = serializer.validated_data['password']

            user = get_object_or_404(User, username=username)
            user.set_password(password)
            user.save()

            return response.HTTP_200
        else:
            return response.http_400("비밀번호를 확인해주세요.")
