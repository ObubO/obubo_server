from django.urls import path
from . import views

urlpatterns = [
    path('join', views.UserCreateView.as_view()),                           # 회원가입
    path('join/id/<str:username>', views.UserCreateView.as_view()),         # 회원가입 시 아이디 유효성 확인
    path('join/nickname/<str:nickname>', views.CheckNickname.as_view()),    # 회원가입 시 닉네임 유효성 확인

    path('login', views.LoginView.as_view()),               # 로그인
    path('logout', views.LogoutView.as_view()),             # 로그아웃
    path('withdrawal', views.WithdrawalView.as_view()),     # 회원탈퇴
    path('kakao/signup', views.KakaoSignUp.as_view()),      # 간편(카카오) 회원가입
    path('kakao/login', views.KakaoLogin.as_view()),        # 간편(카카오) 로그인

    path('auth/sms', views.AuthSMS.as_view()),                              # 인증번호 전송
    path('auth/verify', views.AuthVerify.as_view()),                        # 인증번호 확인
    path('auth/token/refresh', views.CustomTokenRefreshView.as_view()),     # access_token 재발급

    path('users/profiles', views.UserProfileView.as_view()),        # 회원정보 조회 및 수정
    path('users/password', views.UserPasswordView.as_view()),       # 비밀번호 확인 및 변경

    path('check/id/<str:username>', views.AuthUserWithId.as_view()),        # 아이디 is_exist 확인
    path('check/name-phone', views.AuthUserWithName.as_view()),             # 이름-전화번호 일치 확인
    path('check/id-phone', views.AuthUserWithId.as_view()),                 # 아이디-전화번호 일치 확인

    path('find/id', views.FindId.as_view()),                    # 아이디 찾기 GET
    path('change/password', views.PasswordSetView.as_view()),   # 비밀번호 찾기 GET
]
