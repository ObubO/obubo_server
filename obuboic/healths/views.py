from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CareGrade
from .serializers import CareGradeSerializer


# Create your views here.
class CareGradeAPI(APIView):
    def get(self, request):
        serializer = CareGradeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            res = Response(
                {
                    "message": "Register Success",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



