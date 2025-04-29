from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.UserCreateView.as_view()),         # 회원가입
    path('login', views.LoginView.as_view()),               # 로그인
    path('logout', views.LogoutView.as_view()),             # 로그아웃
    path('withdrawal', views.WithdrawalView.as_view()),     # 회원탈퇴

    path('kakao/auth', views.KakaoAuth.as_view()),               # 간편(카카오) 로그인 인증(인가코드 발급) 요청
    path('kakao/callback', views.KakaoCallback.as_view()),       # 간편(카카오) 로그인 인가코드 redirect 및 로그인 처리
    path('kakao/signup', views.KakaoSignUp.as_view()),                      # 간편(카카오) 회원가입 인증(인가코드 발급) 요청 / 회원가입 처리
    path('kakao/callback/signup', views.KakaoCallbackSignup.as_view()),     # 간편(카카오) 회원가입 인가코드 redirect url / 회원가입 처리
    path('check/id/<str:username>', views.UserCreateView.as_view()),        # 회원가입 시 아이디 유효성 확인
    path('check/nickname/<str:nickname>', views.CheckNickname.as_view()),   # 회원가입 시 닉네임 유효성 확인

    path('users/profile', views.UserProfileView.as_view()),                # 회원정보 조회 및 수정
    path('users/id', views.FindUsernameView.as_view()),                      # 아이디 찾기
    path('users/password-confirm', views.PasswordConfirmView.as_view()),     # 비밀번호 검증
    path('users/password-reset', views.PasswordResetRequestView.as_view()),  # 비밀번호 재설정 요청
    path('users/password-reset/<str:uidb64>/<str:token>', views.PasswordResetConfirmView.as_view()),  # 비밀번호 재설정

    path('users/token/refresh', views.CustomTokenRefreshView.as_view()),    # access_token 재발급
    path('users/write/posts', views.UserWritePost.as_view()),               # 작성한 게시글 조회
    path('users/write/comments', views.UserWriteComment.as_view()),         # 작성한 댓글 조회
    path('users/like/posts', views.UserLikePost.as_view()),                 # 좋아요한 게시글 조회
    path('users/like/comments', views.UserLikeComment.as_view()),           # 좋아요한 댓글 조회

    path('verify/phone', views.AuthPhoneNumber.as_view()),        # 전화번호 인증
    path('verify/name-phone', views.AuthUserName.as_view()),      # 이름 및 전화번호 인증
    path('verify/id-phone', views.AuthUserId.as_view()),          # 아이디 및 전화번호 인증

    path('validate/code', views.AuthVerify.as_view()),   # 인증번호 확인

]
