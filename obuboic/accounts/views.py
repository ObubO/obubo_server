from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView


from .models import User
from .serializers import UserSerializer


# Create your views here.
def home(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        email = request.email
        password = request.password

    return render(request, 'login.html')


def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')


class UserCreateAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPI(APIView):
    def get(self):
        queryset = User.objects.all()
        print(queryset)
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)

