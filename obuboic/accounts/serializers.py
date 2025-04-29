from datetime import datetime
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import UserType, User, UserProfile, Terms, UserTerms, AuthTable
from community.serializers import PostSerializer, CommentSerializer
from common import functions


class MemberTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user_id', 'username', 'name', 'nickname', 'gender', 'birth', 'phone', 'email']

    def create(self, validated_data, user=None, user_type=None):
        if user is None:
            raise ValueError("User instance must be provided")
        validated_email = self.get_validated_email(validated_data["email"])

        user_profile = UserProfile(
            user=user,
            user_type=user_type,
            name=validated_data["name"],
            nickname=validated_data["nickname"],
            gender=validated_data["gender"],
            birth=validated_data["birth"],
            phone=validated_data["phone"],
            email=validated_email,
        )

        return user_profile

    def get_validated_email(self, email):
        if email == "":
            email = None

        return email


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class NicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['nickname', ]


class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'


class UserTermsSeriailzer(serializers.ModelSerializer):
    class Meta:
        model = UserTerms
        fields = ['is_consent']


class PhoneNumberValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthTable
        fields = ['phone']


class AuthTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthTable
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    # email = serializers.EmailField(required=True, allow_blank=True)
    typeNo = serializers.IntegerField(required=True)
    terms1 = serializers.BooleanField(required=True)
    terms2 = serializers.BooleanField(required=True)
    terms3 = serializers.BooleanField(required=True)
    terms4 = serializers.BooleanField(required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'password',
                  'name', 'nickname', 'gender', 'birth', 'phone', 'email', 'typeNo',
                  'terms1', 'terms2', 'terms3', 'terms4', ]

    def create(self, validated_data):
        user = self._create_user(validated_data)
        user_profile = self._create_user_profile(user, validated_data)
        self._create_user_terms(user, validated_data)
        return user_profile

    def _create_user(self, validated_data):
        user_data = {'username': validated_data['username'], 'password': validated_data['password']}
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        return user_serializer.save()

    def _create_user_profile(self, user, validated_data):
        type_code = validated_data['typeNo']
        user_type = get_object_or_404(UserType, id=type_code)

        # 회원 정보(Member) 인스턴스 생성
        user_profile_data = {
            'name': validated_data["name"],
            'nickname': validated_data["nickname"],
            'gender': validated_data["gender"],
            'birth': validated_data["birth"],
            'phone': validated_data["phone"],
            'email': validated_data["email"],
        }

        user_profile_serializer = UserProfileSerializer(data=user_profile_data)

        if user_profile_serializer.is_valid(raise_exception=True):
            user_profile = user_profile_serializer.create(validated_data, user, user_type)
            user_profile.save()
            return user_profile

    def _create_user_terms(self, user, validated_data):
        # 약관동의 인스턴스 생성
        terms_list = Terms.objects.all()
        for terms in terms_list:
            terms_name = 'terms' + str(terms.id)
            validated_terms = validated_data[terms_name]
            UserTerms.objects.create(
                user=user,
                terms=get_object_or_404(Terms, id=terms.id),
                is_consent=validated_terms,
                consent_date=datetime.now(),
            )


class KakaoSignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    terms1 = serializers.BooleanField(required=True)
    terms2 = serializers.BooleanField(required=True)
    terms3 = serializers.BooleanField(required=True)
    terms4 = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'name',
                  'terms1', 'terms2', 'terms3', 'terms4', ]

    def create(self, validated_data):
        # 회원 관리(User) 인스턴스 생성
        user_data = {'username': validated_data['username'], 'password': validated_data['password'], 'is_social': True}
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.create(user_serializer.validated_data)

        # 닉네임 생성 및 중복 확인
        while True:
            nickname = functions.create_nickname()
            if not UserProfile.objects.filter(nickname=nickname).exists():
                break

        # 회원 정보(Member) 인스턴스 생성
        user_profile_data = {'name': validated_data['name'], 'nickname': nickname, 'gender': None, 'birth': None, 'phone': None, 'email': None}
        user_type = get_object_or_404(UserType, id=1)

        user_profile_serializer = UserProfileSerializer(data=user_profile_data)
        user_profile_serializer.is_valid(raise_exception=True)
        user_profile = user_profile_serializer.create(user_profile_serializer.validated_data, user, user_type)
        user_profile.save()

        # 약관동의 인스턴스 생성
        terms_list = Terms.objects.all()
        for terms in terms_list:
            terms_name = 'terms' + str(terms.id)
            validated_terms = validated_data[terms_name]
            UserTerms.objects.create(
                user=user,
                terms=get_object_or_404(Terms, id=terms.id),
                is_consent=validated_terms,
                consent_date=datetime.now(),
            )

        return user

    def _create_user(self, validated_data):
        user_data = {'username': validated_data['username'], 'password': validated_data['password']}
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        return user_serializer.save()

    def _create_user_profile(self, user, validated_data):
        while True:
            nickname = functions.create_nickname()
            if not UserProfile.objects.filter(nickname=nickname).exists():
                break  # 중복되지 않으면 루프 종료

        # 회원 정보(Member) 인스턴스 생성
        user_profile_data = {
            'name': validated_data['name'],
            'nickname': nickname,
            'gender': None,
            'birth': None,
            'phone': None,
            'email': None,
        }
        user_type = get_object_or_404(UserType, id=1)
        user_profile_serializer = UserProfileSerializer(data=user_profile_data)
        if user_profile_serializer.is_valid(raise_exception=True):
            user_profile = user_profile_serializer.create(validated_data, user, user_type)
            user_profile.save()
            return user_profile

    def _create_user_terms(self, user, validated_data):
        # 약관동의 인스턴스 생성
        terms_list = Terms.objects.all()
        for terms in terms_list:
            terms_name = 'terms' + str(terms.id)
            validated_terms = validated_data[terms_name]
            UserTerms.objects.create(
                user=user,
                terms=get_object_or_404(Terms, id=terms.id),
                is_consent=validated_terms,
                consent_date=datetime.now(),
            )


class UserWritePostSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = User
        fields = ['posts']


class UserWriteCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = User
        fields = ['comments']


class UserLikePostSerializer(serializers.ModelSerializer):
    like_posts = PostSerializer(many=True)

    class Meta:
        model = User
        fields = ['like_posts']


class UserLikeCommentSerializer(serializers.ModelSerializer):
    like_comments = CommentSerializer(many=True)

    class Meta:
        model = User
        fields = ['like_comments']