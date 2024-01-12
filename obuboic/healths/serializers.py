from rest_framework import serializers
from .models import CareGrade


class CareGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGrade
        fields = '__all__'
