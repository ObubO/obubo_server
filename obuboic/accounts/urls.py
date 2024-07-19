from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('join', views.UserCreateView.as_view()),
    path('join/check-id/<str:username>', views.UserCreateView.as_view()),
    path('join/check-nickname/<str:nickname>', views.CheckNickname.as_view()),

    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('withdrawal', views.WithdrawalView.as_view()),

    path('auth/request/phone', views.AuthPhone.as_view()),
    path('auth/request/name', views.AuthUserWithName.as_view()),
    path('auth/request/id', views.AuthUserWithId.as_view()),
    path('auth/request/id/<str:username>', views.AuthUserWithId.as_view()),
    path('auth/verify', views.AuthVerify.as_view()),

    path('users/profiles', views.AuthView.as_view()),
    path('users/id', views.FindUserAllId.as_view()),
    path('users/check-pw', views.CheckPassword.as_view()),
    path('users/password', views.ChangePasswordView.as_view()),
    path('users/token/refresh', views.CustomTokenRefreshView.as_view()),

]
