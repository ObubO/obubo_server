import jwt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .serializers import UserSerializer

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')


def home(request):
    return render(request, 'index.html')


# 회원가입
class UserCreateAPI(APIView):
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
            )

            res = Response(
                {
                    "message": "Register Success",
                    "user:": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 계정 조회/로그인
class AuthAPI(APIView):
    def get(self, request):
        access = request.COOKIES['access']
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(instance=user)
        print(type(serializer.data))

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        print(user)

        if user is not None:
            # jwt 토큰 발급
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
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
            # jwt 토큰 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
