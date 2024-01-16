import jwt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User
from .serializers import UserSerializer

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')


def home(request):
    return render(request, 'index.html')


# 회원가입
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(
                username=serializer.validated_data["username"],
                nickname=serializer.validated_data["nickname"],
                password=serializer.validated_data["password"],
                email=serializer.validated_data["email"],
                gender=serializer.validated_data["gender"],
                phone=serializer.validated_data["phone"],
                birth=serializer.validated_data["birth"],
                user_type=serializer.validated_data["user_type"],
            )

            response = Response(
                {
                    "message": "Register Success",
                    "user:": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
            return response

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            serializer = UserSerializer(instance=user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Access_Token 기간 만료
        except(jwt.exceptions.ExpiredSignatureError):

            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 사용 불가능 토큰
        except(jwt.exceptions.InvalidTokenError):

            return Response(status=status.HTTP_401_UNAUTHORIZED)


# 계정 로그인 API
class LoginView(APIView):
    def post(self, request):
        try:
            # ID/PW 인증
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))

        except:
            response = Response(
                {
                    "message": "Login Failed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            return response

        else:
            # 인증 통과시(회원이 존재하는 경우)
            if user is not None:
                # JWT 토큰 발급
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)

                # 해당 회원의 Refresh Token 저장
                user.refresh_token = refresh_token
                user.save()

                res = Response(
                    {
                        "message": "Login Success",
                        "token": {
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                    },
                    status=status.HTTP_200_OK,
                )

                return res

            else:
                response = Response(
                    {
                        "message": "Login Failed"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                return response


# 계정 로그아웃 API
class LogoutView(APIView):
    def post(self, request):
        access = request.headers.get('Authorization', None)

        # JWT 인증(Access Token)
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])

        # 사용자 조회
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(instance=user)

        # 해당 회원의 Refresh Token 삭제
        user.refresh_token = None
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# AccessToken 재발급 API
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

        #-- 탈취당한 Refresh Token 여부 --#
            # 정상적 요청인 경우
            if refresh_token == serializer.data.get('refresh_token'):
                data = {'refresh': refresh_token}
                token_serializer = TokenRefreshSerializer(data=data)

                if token_serializer.is_valid():
                    access_token = token_serializer.validated_data

                    return Response(access_token, status=status.HTTP_200_OK)

            # 공격시도 감지
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        # 기간 만료된 토큰
        except(jwt.exceptions.ExpiredSignatureError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 사용 불가능 토큰
        except(jwt.exceptions.InvalidTokenError):

            return Response(status=status.HTTP_401_UNAUTHORIZED)
