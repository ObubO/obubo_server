from rest_framework import serializers
from .models import UserType, User, Member, TAC, TACAgree, AuthTable


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
        fields = '__all__'


class CreateMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['name', 'nickname', 'gender', 'birth', 'phone', 'email', ]


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

