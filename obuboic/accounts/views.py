import jwt
import random
from datetime import datetime, timedelta
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User, Member, TAC, TACAgree, Certify
from .serializers import UserSerializer, MemberSerializer, CheckUserIdSerializer, CertifySerializer
from sms import message


SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')
SMS_API_KEY = getattr(settings, "SMS_API_KEY")
SMS_API_SECRET = getattr(settings, "SMS_API_SECRET")


def home(request):
    return render(request, 'index.html')


# -- 회원가입 -- #

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(APIView):

    # 중복 아이디 확인
    def get(self, request):
        data = request.GET.urlencode()
        query_dict = QueryDict(data)

        serializer = CheckUserIdSerializer(data=query_dict)

        if serializer.is_valid():
            return Response({"code": 200, "message": "사용가능한 ID 입니다"}, status=status.HTTP_200_OK)
        else:
            return Response({"code": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"code": 400, "message": "회원가입 실패", "error": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # 회원정보(Member) 인스턴스 선언
        if member_serializer.is_valid():
            member = Member(
                user=user,
                name=member_serializer.validated_data["name"],
                gender=member_serializer.validated_data["gender"],
                birth=member_serializer.validated_data["birth"],
                phone=member_serializer.validated_data["phone"],
                email=member_serializer.validated_data["email"],
            )

        else:
            return Response({"code": 400, "message": "회원가입 실패", "error": member_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # 약관동의 인스턴스 생성
        try:
            tacs = [[1, 'tac1'], [2, 'tac2'], [3, 'tac3'], [4, 'tac4']]
            for tac in tacs:
                code, consent = tac[0], tac[1]
                TACAgree.objects.create(
                    user=user,
                    tac=get_object_or_404(TAC, id=code),
                    is_consent=request.data[consent],
                    consent_date=datetime.now(),
                )
            member.save()

            return Response({"code": 201, "message": "회원가입 완료"}, status=status.HTTP_201_CREATED)

        except:
            User.objects.filter(username=username).delete()
            return Response({"code": 400, "message": "회원가입 실패", "error": "e"}, status=status.HTTP_400_BAD_REQUEST)


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

            return Response({"code": 200, "message": "사용자 조회 성공", "result": {"user": serializer.data}}, status=status.HTTP_200_OK)

        # Access_Token 기간 만료
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"code": 401, "message": "토큰의 유효기간이 만료되었습니다"}, status=status.HTTP_401_UNAUTHORIZED)

        # 사용 불가능 토큰
        except jwt.exceptions.InvalidTokenError:
            return Response({"code": 400, "message": "유효하지 않은 토큰입니다"}, status=status.HTTP_400_BAD_REQUEST)


# 계정 로그인 API
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        try:
            # ID/PW 인증
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        except():
            return Response({"code": 400, "message": "로그인 정보가 올바르지 않습니다"}, status=status.HTTP_400_BAD_REQUEST)

        else:
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

                return Response({"code": 200, "message": "로그인 성공", "result": {"token": {"access": access_token, "refresh": refresh_token}}}, status=status.HTTP_200_OK)

            else:
                return Response({"code": 400, "message": "로그인 정보가 올바르지 않습니다"}, status=status.HTTP_400_BAD_REQUEST)


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

            return Response({"code": 200, "message": "로그아웃 성공"}, status=status.HTTP_200_OK)

        except jwt.exceptions.InvalidTokenError:
            return Response({"code": 400, "message": "유효하지 않은 토큰입니다"}, status=status.HTTP_400_BAD_REQUEST)


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

                    return Response({"code": 200, "message": "Access Token 발급 성공", "result": {"token": {"access": access_token}}}, status=status.HTTP_200_OK)

                return Response({"code": 503, "message": "토큰 발급 에러 발생. 서버확인 필요"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 공격시도 감지
            else:
                return Response({"code": 403, "message": "사용자가 삭제한 토큰입니다"}, status=status.HTTP_403_FORBIDDEN)

        # 기간 만료된 토큰
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"code": 401, "message": "기간이 만료된 토큰입니다"}, status=status.HTTP_401_UNAUTHORIZED)

        # 사용 불가능 토큰
        except jwt.exceptions.InvalidTokenError:
            return Response({"code": 400, "message": "사용할 수 없는 토큰입니다"}, status=status.HTTP_400_BAD_REQUEST)


class AuthRequest(APIView):
    def post(self, request):
        # 데이터 유효성 검사
        cert_serializer = CertifySerializer(data=request.data)

        # 인증 정보 저장
        if cert_serializer.is_valid():
            phone = cert_serializer.validated_data["phone"]
            code = str(random.randint(100000, 999999))

            Certify.objects.create(phone=phone, code=code)

            # 인증 코드 전송
            res_code = message.send_sms(SMS_API_KEY, SMS_API_SECRET, phone, code)

            if res_code == 200:
                return Response({"code": 200, "message": "인증문자 전송 성공"}, status=status.HTTP_200_OK)
            else:
                return Response({"code": 503, "message": "인증문자 전송 실패"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({"code": 400, "message": "전화번호 유효성 검사 실패"}, status=status.HTTP_400_BAD_REQUEST)


class AuthVerify(APIView):
    def post(self, request):
        phone = request.data["phone"]
        code = request.data["code"]

        # 현재 시간 체크
        current_time = datetime.now()

        # 인증 데이터 조회
        cert = Certify.objects.filter(phone=phone).order_by('-created_at').first()
        serialier = CertifySerializer(instance=cert)
        db_code = serialier.data['code']
        db_time = datetime.strptime(serialier.data['created_at'], "%Y-%m-%dT%H:%M:%S.%f")

        # 인증번호 유효성 검사
        time_difference = current_time - db_time
        if code == db_code:
            if time_difference <= timedelta(minutes=3):
                return Response({"code": 200, "message": "인증 성공"}, status=status.HTTP_200_OK)
            else:
                return Response({"code": 401, "message": "인증번호 시간 초과"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"code": 400, "message": "인증번호 불일치"}, status=status.HTTP_400_BAD_REQUEST)
