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


class CareGradeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGradeDetail
        fields = '__all__'


class UserCareDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGradeDetail
        fields = ['data', 'age', 'gender']

    def create(self, validated_data):
        care = CareGradeDetail(
            data=validated_data['data'],
            age=validated_data['age'],
            gender=validated_data['gender'],
        )

        return care
