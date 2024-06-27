from rest_framework import serializers
from .models import UserType, User, Member, TAC, TACAgree, Certify


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
        fields = ['name', 'gender', 'birth', 'phone', 'email', ]


class TACSerializer(serializers.ModelSerializer):

    class Meta:
        model = TAC
        fields = '__all__'


class TACAgreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TACAgree
        fields = ['is_consent', ]


class CertifyPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certify
        fields = ['phone']


class CertifyAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certify
        fields = '__all__'

