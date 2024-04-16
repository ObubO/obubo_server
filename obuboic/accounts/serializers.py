from rest_framework import serializers
from .models import UserType, User, Member, PrivacyPolicy, PolicyAgree


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'gender', 'phone', 'birth', 'user_type']


class CheckUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['name', 'gender', 'birth', 'phone', 'email', ]


class PrivacyPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivacyPolicy
        fields = '__all__'


class PolicyAgreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PolicyAgree
        fields = '__all__'


