from django.urls import path
from . import views

urlpatterns = [
    # 회원가입/로그인
    path('signup', views.UserSignupView.as_view()),             # POST: 회원가입
    path('login', views.UserLoginView.as_view()),               # POST: 로그인
    path('logout', views.UserLogoutView.as_view()),             # POST: 로그아웃
    path('withdrawal', views.UserWithdrawalView.as_view()),     # POST: 회원탈퇴

    # 회원가입 검증
    path('check-username/<str:username>', views.UserIdCheckView.as_view()),         # GET: 아이디 중복 검사
    path('check-nickname/<str:nickname>', views.UserNicknameCheckView.as_view()),   # GET: 닉네임 중복 검사

    # 사용자 프로필
    path('users/profile', views.UserProfileView.as_view()),                                               # GET: 회원정보 조회 / PATCH: 회원정보 수정
    path('users/find-id', views.UserFindIdView.as_view()),                                                # POST: 아이디 찾기
    path('users/password-reset', views.UserPasswordResetView.as_view()),                                  # POST: 비밀번호 확인
    path('users/password-confirm', views.UserPasswordConfirmView.as_view()),                              # POST: 비밀번호 확인

    # 사용자 활동 조회
    path('users/write/posts', views.UserWritePostView.as_view()),         # GET: 내가 쓴 게시글 조회
    path('users/write/comments', views.UserWriteCommentView.as_view()),   # GET: 내가 쓴 댓글 조회
    path('users/like/posts', views.UserLikePostView.as_view()),           # GET: 좋아요한 게시글
    path('users/like/comments', views.UserLikeCommentView.as_view()),     # GET: 좋아요한 댓글

    # 인증
    path('verify/phone', views.PhoneVerificationView.as_view()),            # POST: 전화번호 인증
    path('verify/name-phone', views.NamePhoneVerificationView.as_view()),   # POST: 이름+전화번호 인증
    path('verify/id-phone', views.IdPhoneVerificationView.as_view()),       # POST: 이름+전화번호 인증
    path('validate/code', views.VerificationCodeConfirmView.as_view()),     # POST: 인증번호 확인

    # 토큰
    path('users/token/refresh', views.UserTokenRefreshView.as_view()),        # POST: access_token 재발급

    # 카카오 로그인
    path('kakao/login', views.KakaoLogin.as_view()),                     # GET: 카카오 로그인 인가코드 요청 / POST: 로그인 처리
    path('kakao/login/callback', views.KakaoCallbackLogin.as_view()),    # GET: 카카오 로그인 인가코드 콜백
    path('kakao/signup', views.KakaoSignUp.as_view()),                   # GET: 카카오 회원가입 인가코드 요청 / POST: 회원가입 처리
    path('kakao/signup/callback', views.KakaoCallbackSignup.as_view()),  # GET: 카카오 회원가입 인가코드 콜백

]
