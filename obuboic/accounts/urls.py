from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('join', views.UserCreateView.as_view()),
    path('join/check-id/<str:username>', views.UserCreateView.as_view()),
    path('join/check-name/<str:name>', views.CheckMemberName.as_view()),

    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('withdrawal', views.WithdrawalView.as_view()),

    path('auth/request', views.AuthRequest.as_view()),
    path('auth/request/users', views.AuthUserRequest.as_view()),
    path('auth/request/users/<str:username>', views.AuthUserRequest.as_view()),
    path('auth/verify', views.AuthVerify.as_view()),

    path('users/profiles', views.AuthView.as_view()),
    path('users/password', views.ChangePassword.as_view()),
    path('users/token/refresh', views.CustomTokenRefreshView.as_view()),

]
