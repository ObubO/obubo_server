from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import UserType, User, UserProfile, Terms, UserTerms, AuthTable
from community.serializers import PostSerializer, CommentSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers


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

        email = self.get_validated_email(validated_data["email"])

        user_profile = UserProfile(
            user=user,
            user_type=user_type,
            name=validated_data["name"],
            nickname=validated_data["nickname"],
            gender=validated_data["gender"],
            birth=validated_data["birth"],
            phone=validated_data["phone"],
            email=email,
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
        user = None
        user_profile = None

        try:
            user = self._create_user(validated_data)
            user_profile = self._create_user_profile(validated_data, user)
            self._create_user_terms(validated_data, user)

        except Exception as e:
            if user_profile:
                user_profile.delete()
            if user:
                user.delete()

            raise ValueError(f'error: 계정 생성 에러, error_descrption: {str(e)}')

        return user_profile

    def _create_user(self, validated_data):
        user_serializer = UserSerializer(data=validated_data)

        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()

            return user

    def _create_user_profile(self, validated_data, user):
        user_type = get_object_or_404(UserType, id=validated_data['typeNo'])
        user_profile_serializer = UserProfileSerializer(data=validated_data)

        if user_profile_serializer.is_valid(raise_exception=True):
            user_profile = user_profile_serializer.create(validated_data, user, user_type)
            user_profile.save()

            return user_profile

    def _create_user_terms(self, validated_data, user):
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
    nickname = serializers.CharField(required=True)
    typeNo = serializers.IntegerField(required=True)
    terms1 = serializers.BooleanField(required=True)
    terms2 = serializers.BooleanField(required=True)
    terms3 = serializers.BooleanField(required=True)
    terms4 = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'nickname', 'typeNo', 'terms1', 'terms2', 'terms3', 'terms4', ]

    def create(self, validated_data):
        user = None
        user_profile = None

        try:
            user = self._create_user(validated_data)
            user_profile = self._create_user_profile(validated_data, user)
            self._create_user_terms(validated_data, user)

        except Exception as e:
            if user_profile:
                user_profile.delete()
            if user:
                user.delete()

            raise ValueError(f'error: 계정 생성 에러, error_descrption: {str(e)}')

        return user_profile

    def _create_user(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'password': validated_data['password'],
        }

        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.is_social = True
            user.save()

            return user

    def _create_user_profile(self, validated_data, user):
        user_type = get_object_or_404(UserType, id=validated_data['typeNo'])

        user_profile_data = {
            'name': validated_data['name'],
            'nickname': validated_data['nickname'],
            'user_type': user_type,
            'gender': None,
            'birth': None,
            'phone': None,
            'email': None,
        }

        user_profile_serializer = UserProfileSerializer(data=user_profile_data)

        if user_profile_serializer.is_valid(raise_exception=True):
            user_profile = user_profile_serializer.create(user_profile_serializer.validated_data, user, user_type)
            user_profile.save()

            return user_profile

    def _create_user_terms(self, validated_data, user):
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 여기서 payload 커스터마이징도 가능 (ex. token['username'] = user.username)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

    def generate_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        data = {
            "refresh": str(refresh),
            "access": str(access),
        }

        return data

