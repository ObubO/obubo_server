from datetime import datetime

from rest_framework import serializers
from .models import UserType, User, Member, TAC, TACAgree, AuthTable
from django.shortcuts import get_object_or_404


class UserTypeSerializer(serializers.ModelSerializer):
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


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username'


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class CheckUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['name', 'nickname', 'gender', 'birth', 'phone', 'email']

    def create(self, validated_data):
        validated_email = self.get_validated_email(validated_data["email"])

        member = Member(
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


class CheckNicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['nickname', ]


class TACSerializer(serializers.ModelSerializer):

    class Meta:
        model = TAC
        fields = '__all__'


class TACAgreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TACAgree
        fields = ['is_consent', ]


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
    tac1 = serializers.BooleanField(required=True)
    tac2 = serializers.BooleanField(required=True)
    tac3 = serializers.BooleanField(required=True)
    tac4 = serializers.BooleanField(required=True)

    class Meta:
        model = Member
        fields = ['username', 'password',
                  'name', 'nickname', 'gender', 'birth', 'phone', 'email', 'typeNo',
                  'tac1', 'tac2', 'tac3', 'tac4', ]

    def create(self, validated_data):

        # 회원 관리(User) 인스턴스 생성
        user_data = {
            'username': validated_data['username'],
            'password': validated_data['password'],
        }
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.create(user_serializer.validated_data)

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
        member_serializer.is_valid(raise_exception=True)
        member = member_serializer.create(member_serializer.validated_data)
        member.user = user

        type_code = validated_data['typeNo']
        member.user_type = get_object_or_404(UserType, id=type_code)
        member.save()

        # 약관동의 인스턴스 생성
        tacs = TAC.objects.all()
        for tac in tacs:
            tac_name = 'tac' + str(tac.id)
            validated_term = validated_data[tac_name]
            TACAgree.objects.create(
                user=user,
                tac=get_object_or_404(TAC, id=tac.id),
                is_consent=validated_term,
                consent_date=datetime.now(),
            )
        return None

