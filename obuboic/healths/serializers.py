from rest_framework import serializers
from .models import CareGradeEx, CareGradeSimple, CareGradeDetail


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
            region=validated_data["region"],
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
            region=validated_data["region"],
        )

        return caregrade
