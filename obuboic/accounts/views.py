import jwt
import random
from datetime import datetime, timedelta
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User, Member, AuthTable
from .serializers import CheckPasswordSerializer, MemberSerializer, CheckNicknameSerializer, CheckUserIdSerializer, AuthTablePhoneSerializer, AuthTableSerializer, SignUpSerializer
from sms import message
from common import response

SECRET_KEY = getattr(settings, 'SECRET_KEY', 'SECRET_KEY')
SMS_API_KEY = getattr(settings, "SMS_API_KEY")
SMS_API_SECRET = getattr(settings, "SMS_API_SECRET")


def auth_request(phone):
    # 인증코드 생성 및 저장
    code = str(random.randint(100000, 999999))
    AuthTable.objects.create(phone=phone, code=code)

    # 인증 코드 전송
    res_code = message.send_sms(SMS_API_KEY, SMS_API_SECRET, phone, code)

    return res_code


def jwt_decode_handler(token):
    try:
        # JWT 인증(Access Token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)

        return True, user

    # Token has expired
    except jwt.exceptions.ExpiredSignatureError as e:
        return False, response.http_401("Token has expired")
    # Invalid token
    except jwt.exceptions.InvalidTokenError as e:
        return False, response.http_400("Invalid Token")


# -- 회원가입 -- #
class UserCreateView(APIView):
    # 중복 아이디 확인
    def get(self, request, username):
        try:
            query_dict = QueryDict('username='+username)
            serializer = CheckUserIdSerializer(data=query_dict)

            if serializer.is_valid():
                return response.HTTP_200
            else:
                return response.http_400(serializer.errors)

        except:
            return response.http_500("서버 확인 필요")

    # 회원가입
    def post(self, request):
        try:
            print(request.data)
            serializer = SignUpSerializer(data=request.data)

            if serializer.is_valid():
                serializer.create(serializer.validated_data)

                return response.HTTP_200
            else:
                return response.http_400(serializer.errors)

        except:
            return response.http_500("서버 확인 필요")


# 닉네임 중복 확인
class CheckNickname(APIView):
    def get(self, request, nickname):
        try:
            query_dict = QueryDict('nickname='+nickname)
            serializer = CheckNicknameSerializer(data=query_dict)

            if serializer.is_valid():
                return response.HTTP_200
            else:
                return response.http_400(serializer.errors)

        except:
            return response.http_500("서버 확인 필요")


# 계정 조회/수정 API
class AuthView(APIView):
    def query_to_dict(self, query_dict):
        data_dict = {}

        for key in query_dict.keys():
            values = query_dict.getlist(key)
            data_dict[key] = values[0]

        return data_dict

    def get(self, request):
        access_token = request.headers.get('Authorization', None)

        jwt_decode_data = jwt_decode_handler(access_token)
        jwt_is_valid, user = jwt_decode_data[0], jwt_decode_data[1]

        if not jwt_is_valid:
            result = jwt_decode_data[1]
            return response.http_400(result)

        member = get_object_or_404(Member, user=user)
        member_serializer = MemberSerializer(instance=member)
        result = {"user": member_serializer.data}

        return response.http_200(result)

    def patch(self, request):
        access_token = request.headers.get('Authorization', None)

        token_data = jwt_decode_handler(access_token)
        jwt_is_valid = token_data[0]

        if jwt_is_valid:
            user = token_data[1]
            member = get_object_or_404(Member, user=user)
            try:
                data_dict = self.query_to_dict(request.data)  # test(postman) 요청 시 데이터 변환
            except:
                data_dict = request.data  # 클라이언트 요청 시

            for key, value in data_dict.items():
                setattr(member, key, value)

            member.save()
            return response.HTTP_200
        else:
            http_error_response = token_data[1]
            return http_error_response


# 계정 로그인 API
class LoginView(APIView):
    def post(self, request):
        try:
            # ID/PW 인증
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
            is_active = user.is_active
            # 인증 통과시(회원이 존재하는 경우)
            if user is not None and is_active:
                # JWT 토큰 발급
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)

                # 해당 회원의 Refresh Token 저장
                user.refresh_token = refresh_token
                user.last_login = datetime.now()
                user.save()

                result = {"token": {"access": access_token, "refresh": refresh_token}}
                return response.http_200(result)
            else:
                return response.http_400("회원정보가 올바르지 않습니다.")

        except:
            return response.http_400("회원정보를 확인해주세요.")


# 계정 로그아웃 API
class LogoutView(APIView):
    def post(self, request):
        refresh = request.headers.get('Authorization', None)

        # JWT 인증 - 기간만료 무시
        try:
            payload = jwt.decode(refresh, SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
        except jwt.exceptions.InvalidTokenError:
            return response.http_400("유효하지 않은 토큰입니다.")

        # 사용자 조회
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)

        # 해당 회원의 Refresh Token 삭제
        user.refresh_token = None
        user.save()

        return response.HTTP_200


# 회원 탈퇴 API
class WithdrawalView(APIView):
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization', None)

            jwt_decode_data = jwt_decode_handler(access_token)
            jwt_is_valid, user = jwt_decode_data[0], jwt_decode_data[1]

            if not jwt_is_valid:
                http_error_response = jwt_decode_data[1]
                return http_error_response

            user.delete()

            return response.HTTP_200
        except:
            return response.http_500("서버 확인 필요")


# AccessToken 재발급 API
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        jwt_decode_data = jwt_decode_handler(refresh_token)
        jwt_is_valid, user = jwt_decode_data[0], jwt_decode_data[1]

        if not jwt_is_valid:
            http_error_response = jwt_decode_data[1]
            return http_error_response

        # -- 탈취당한 Refresh Token 여부 -- #
        # 정상적 요청인 경우
        if refresh_token == user.refresh_token:
            data = {'refresh': refresh_token}
            token_serializer = TokenRefreshSerializer(data=data)

            if token_serializer.is_valid():
                access_token = token_serializer.validated_data
                result = {"token": access_token}
                return response.http_200(result)
            else:
                return response.http_503("서버 에러 발생")

        # 공격시도 감지
        else:
            return response.http_403("사용자가 삭제한 토큰입니다.")


# -- 전화번호 인증  -- #
class AuthPhone(APIView):
    def post(self, request):
        # 데이터 유효성 검사
        serializer = AuthTablePhoneSerializer(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data["phone"]

            res_code = auth_request(phone)

            if res_code == 200:
                return response.HTTP_200
            else:
                return response.http_503("인증문자 전송 실패")
        else:
            return response.http_400("전화번호를 확인해주세요.")


# -- 회원 아이디 인증 -- #
class AuthUserWithId(APIView):
    def get(self, request, username):
        user_exist = User.objects.filter(username=username).exists()

        if user_exist:
            return response.HTTP_200
        else:
            return response.http_404("ID를 확인해주세요.")

    def post(self, request):
        username = request.data['username']
        phone = request.data['phone']

        member = get_object_or_404(Member, phone=phone)
        db_username = member.user.username

        if username == db_username:
            res_code = auth_request(phone)

            if res_code == 200:
                return response.HTTP_200
            else:
                return response.http_503("인증문자 전송 실패")
        else:
            return response.http_401("회원가입 시 기입한 아이디를 입력해주세요.")


# -- 회원 이름 인증 -- #
class AuthUserWithName(APIView):
    def post(self, request):
        name = request.data['name']
        phone = request.data['phone']

        member = get_object_or_404(Member, phone=phone)

        if name == member.name:
            res_code = auth_request(phone)

            if res_code == 200:
                return response.HTTP_200
            else:
                return response.http_503("인증문자 전송 실패")
        else:
            return response.http_401("회원가입 시 기입한 이름을 입력해주세요.")


# -- 인증코드 확인 -- #
class AuthVerify(APIView):
    def post(self, request):
        phone = request.data["phone"]
        code = request.data["code"]

        # 현재 시간 체크
        current_time = datetime.now()

        # 인증 데이터 조회
        auth_instance = AuthTable.objects.filter(phone=phone).order_by('-created_at').first()

        if auth_instance is None:
            return response.http_404("전화번호가 존재하지 않습니다.")

        serializer = AuthTableSerializer(instance=auth_instance)
        db_code = serializer.data['code']
        db_time = datetime.strptime(serializer.data['created_at'], "%Y-%m-%dT%H:%M:%S.%f")

        # 인증번호 유효성 검사
        time_difference = current_time - db_time
        if code == db_code:
            if time_difference <= timedelta(minutes=5):
                return response.HTTP_200
            else:
                return response.http_401("인증번호 유효기간이 만료되었습니다.")
        else:
            return response.http_400("인증번호를 확인해주세요.")


# -- 비밀번호 확인 -- #
class CheckPassword(APIView):
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization', None)

            jwt_decode_data = jwt_decode_handler(access_token)
            jwt_is_valid, user = jwt_decode_data[0], jwt_decode_data[1]

            if not jwt_is_valid:
                http_error_response = jwt_decode_data[1]
                return http_error_response

            password = request.data['password']
            if user.check_password(password):
                return response.HTTP_200
            else:
                return response.http_403("비밀번호가 일치하지 않습니다.")

        except Exception as e:
            return response.http_400(str(e))


# -- 비밀번호 변경 -- #
class ChangePasswordView(APIView):
    def post(self, request):
        serializer = CheckPasswordSerializer(data=request.data)

        if serializer.is_valid():
            # 비인증(비로그인) 회원 조회
            try:
                username = request.data['username']
                user = get_object_or_404(User, username=username)
            # 인증(로그인) 회원 조회
            except:
                access_token = request.headers.get('Authorization', None)

                jwt_data = jwt_decode_handler(access_token)
                jwt_is_valid, user = jwt_data[0], jwt_data[1]

                if not jwt_is_valid:
                    http_error_response = jwt_data[1]
                    return http_error_response

            password = serializer.validated_data['password']

            user.set_password(password)
            user.save()

            return response.HTTP_200
        else:
            return response.http_400(serializer.errors)


# -- 아이디 찾기(부분) -- #
class FindUserPartId(APIView):
    def post(self, request):
        name = request.data['name']
        phone = request.data['phone']

        member = get_object_or_404(Member, phone=phone)

        if member.name == name:
            username = member.user.username[0:3]
            for i in range(len(username[3:])):
                username = username + "*"

            return response.http_200(username)
        else:
            return response.http_404("해당 회원이 존재하지 않습니다.")


# -- 아이디 찾기(전체) -- #
class FindUserAllId(APIView):
    def post(self, request):
        phone = request.data['phone']

        member = get_object_or_404(Member, phone=phone)
        username = member.user.username

        str_date = str(member.user.created_at)
        date = datetime.fromisoformat(str_date)
        formatted_date = date.strftime('%Y-%m-%d')

        result = response.make_result2("id", username, "date", formatted_date)

        return response.http_200(result)
