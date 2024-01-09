from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer


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


