from django.urls import path
from . import views

urlpatterns = [
    # 회원가입/로그인
    path('users/signup', views.UserSignupView.as_view()),             # POST: 회원가입
    path('users/login', views.UserLoginView.as_view()),               # POST: 로그인
    path('users/logout', views.UserLogoutView.as_view()),             # POST: 로그아웃
    path('users/withdrawal', views.UserWithdrawalView.as_view()),     # POST: 회원탈퇴

    # 회원가입 검증
    path('users/check-username/<str:username>', views.UserIdCheckView.as_view()),         # GET: 아이디 중복 검사
    path('users/check-nickname/<str:nickname>', views.UserNicknameCheckView.as_view()),   # GET: 닉네임 중복 검사

    # 사용자 프로필
    path('users/profile', views.UserProfileView.as_view()),                                               # GET: 회원정보 조회 / PATCH: 회원정보 수정
    path('users/find-id', views.UserFindIdView.as_view()),                                                # POST: 아이디 찾기
    path('users/password-confirm', views.UserPasswordConfirmView.as_view()),                              # POST: 비밀번호 확인
    path('users/password-reset', views.UserPasswordResetRequestView.as_view()),                           # POST: 비밀번호 재설정 요청
    path('users/password-reset/<str:uidb64>/<str:token>', views.UserPasswordResetConfirmView.as_view()),  # POST: 비밀번호 재설정 처리

    # 사용자 활동 조회
    path('users/write/posts', views.UserWritePostView.as_view()),         # GET: 내가 쓴 게시글 조회
    path('users/write/comments', views.UserWriteCommentView.as_view()),   # GET: 내가 쓴 댓글 조회
    path('users/like/posts', views.UserLikePostView.as_view()),           # GET: 좋아요한 게시글
    path('users/like/comments', views.UserLikeCommentView.as_view()),     # GET: 좋아요한 댓글

    # 인증
    path('verifications/phone', views.PhoneVerificationView.as_view()),            # POST: 전화번호 인증
    path('verifications/name-phone', views.NamePhoneVerificationView.as_view()),   # POST: 이름+전화번호 인증
    path('verifications/code', views.VerificationCodeConfirmView.as_view()),       # POST: 인증번호 확인

    # 토큰
    path('users/token/refresh', views.UserTokenRefreshView.as_view()),        # POST: access_token 재발급

    # 카카오 로그인
    path('auth/kakao/login', views.KakaoAuth.as_view()),                      # GET: 카카오 로그인 인가코드 요청
    path('auth/kakao/login/callback', views.KakaoCallback.as_view()),         # GET: 카카오 로그인 인가코드 콜백 및 로그인
    path('auth/kakao/signup', views.KakaoSignUp.as_view()),                   # GET: 카카오 회원가입 인가코드 요청 / POST: 회원가입 처리
    path('auth/kakao/signup/callback', views.KakaoCallbackSignup.as_view()),  # GET: 카카오 회원가입 인가코드 콜백

]
