from datetime import datetime
from rest_framework import serializers
from .models import MemberType, User, Member, Terms, UserTerms, AuthTable
from django.shortcuts import get_object_or_404
from community.serializers import PostSerializer, PostUserSerializer, CommentSerializer, CommentUserSerializer, PostLikeUserSerializer, CommentLikeUserSerializer
from common import functions


class MemberTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberType
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
    posts = PostUserSerializer(many=True, read_only=True, default=[])
    comments = CommentUserSerializer(many=True, read_only=True, default=[])
    like_posts = PostLikeUserSerializer(many=True, source='postlike_set', read_only=True, default=[])
    like_comments = CommentLikeUserSerializer(many=True, source='commentlike_set', read_only=True, default=[])

    class Meta:
        model = User
        fields = ['id', 'username', 'posts', 'comments', 'like_posts', 'like_comments']


class MemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['name', 'nickname', 'gender', 'birth', 'phone', 'email', 'user']

    def create(self, validated_data, user=None, member_type=None):
        if user is None:
            raise ValueError("User instance must be provided")
        validated_email = self.get_validated_email(validated_data["email"])

        member = Member(
            user=user,
            member_type=member_type,
            name=validated_data["name"],
            nickname=validated_data["nickname"],
            gender=validated_data["gender"],
            birth=validated_data["birth"],
            phone=validated_data["phone"],
            email=validated_email,
        )

        return member

    def get_validated_email(self, email):
        if email == "":
            email = None

        return email


class CheckPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class CheckUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class CheckNicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['nickname', ]


class TermsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Terms
        fields = '__all__'


class UserTermsSeriailzer(serializers.ModelSerializer):

    class Meta:
        model = UserTerms
        fields = ['is_consent']


class AuthTablePhoneSerializer(serializers.ModelSerializer):

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
    email = serializers.EmailField(required=True, allow_blank=True)
    typeNo = serializers.IntegerField(required=True)
    terms1 = serializers.BooleanField(required=True)
    terms2 = serializers.BooleanField(required=True)
    terms3 = serializers.BooleanField(required=True)
    terms4 = serializers.BooleanField(required=True)

    class Meta:
        model = Member
        fields = ['username', 'password',
                  'name', 'nickname', 'gender', 'birth', 'phone', 'email', 'typeNo',
                  'terms1', 'terms2', 'terms3', 'terms4', ]

    def create(self, validated_data):
        user = self._create_user(validated_data)
        member = self._create_member(user, validated_data)
        self._create_user_terms(user, validated_data)
        return member

    def _create_user(self, validated_data):
        user_data = {'username': validated_data['username'], 'password': validated_data['password']}
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        return user_serializer.save()

    def _create_member(self, user, validated_data):
        type_code = validated_data['typeNo']
        member_type = get_object_or_404(MemberType, id=type_code)

        # 회원 정보(Member) 인스턴스 생성
        member_data = {
            'name': validated_data["name"],
            'nickname': validated_data["nickname"],
            'gender': validated_data["gender"],
            'birth': validated_data["birth"],
            'phone': validated_data["phone"],
            'email': validated_data["email"],
        }

        member_serializer = MemberSerializer(data=member_data)

        if member_serializer.is_valid(raise_exception=True):
            member = member_serializer.create(validated_data, user, member_type)
            member.save()
            return member

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
            if not Member.objects.filter(nickname=nickname).exists():
                break

        # 회원 정보(Member) 인스턴스 생성
        member_data = {'name': validated_data['name'], 'nickname': nickname, 'gender': None, 'birth': None, 'phone': None, 'email': None}
        member_type = get_object_or_404(MemberType, id=1)

        member_serializer = MemberSerializer(data=member_data)
        member_serializer.is_valid(raise_exception=True)
        member = member_serializer.create(member_serializer.validated_data, user, member_type)
        member.save()

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

    def _create_member(self, user, validated_data):
        while True:
            nickname = functions.create_nickname()
            if not Member.objects.filter(nickname=nickname).exists():
                break  # 중복되지 않으면 루프 종료

        # 회원 정보(Member) 인스턴스 생성
        member_data = {
            'name': validated_data['name'],
            'nickname': nickname,
            'gender': None,
            'birth': None,
            'phone': None,
            'email': None,
        }
        member_type = get_object_or_404(MemberType, id=1)
        member_serializer = MemberSerializer(data=member_data)
        if member_serializer.is_valid(raise_exception=True):
            member = member_serializer.create(validated_data, user, member_type)
            member.save()
            return member

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

