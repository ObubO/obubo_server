from rest_framework import serializers
from .models import CareGradeEx, CareGradeSimple, CareGradeDetail, GovService
from django.db.models import Q


class CareGradeExSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGradeEx
        fields = '__all__'


class CareGradeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGradeSimple
        fields = '__all__'

    def create(self, validated_data, user=None):
        caregrade = CareGradeSimple(
            user=user,
            data=validated_data["data"],
            gender=validated_data["gender"],
            age=validated_data["age"],
            # region=validated_data["region"],          정부 보조금 추천 기능 도입 후 삽입
        )

        return caregrade


class CareGradeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGradeDetail
        fields = '__all__'

    def create(self, validated_data, user=None):
        caregrade = CareGradeDetail(
            user=user,
            data=validated_data["data"],
            gender=validated_data["gender"],
            age=validated_data["age"],
            # region=validated_data["region"],          정부 보조금 추천 기능 도입 후 삽입
        )

        return caregrade


class GovServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovService
        fields = '__all__'

    def filter_age_region(self, validated_data):
        instance_list = GovService.objects.filter(
            Q(age_limit__isnull=True) | Q(age_limit__lte=validated_data['age']),
            Q(region__isnull=True) | Q(region=validated_data['region'])
        ).order_by('-created_at')

        return instance_list
