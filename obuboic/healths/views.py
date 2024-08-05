from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CareGradeExSerializer, CareGradeSimpleSerializer, CareGradeDetailSerializer
from .analysis import AnalysisDiagram, SimpleAnalysisDiagram
from common import response


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CareGradeExAPI(APIView):
    def post(self, request):
        serializer = CareGradeExSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data["data"]

            # 간소평가 분석
            try:
                analysis = SimpleAnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)
            except:
                return response.http_400("데이터 에러")

            # 간소평가 등록
            serializer.save()

            result = {"score": score, "rate": rate}
            return response.http_200(result)

        else:
            return response.http_400(serializer.errors)


@method_decorator(csrf_exempt, name='dispatch')
class CareGradeSimpleAPI(APIView):
    def post(self, request):
        serializer = CareGradeSimpleSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data["data"]

            # 간소평가 분석
            try:
                analysis = SimpleAnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)
            except:
                return response.http_400("데이터 에러")

            serializer.save()

            result = {"score": score, "rate": rate}
            return response.http_200(result)

        else:
            return response.http_400(serializer.errors)


@method_decorator(csrf_exempt, name='dispatch')
class CareGradeDetailAPI(APIView):
    def post(self, request):
        serializer = CareGradeDetailSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data["data"]

            # 요양등급평가 분석
            try:
                analysis = AnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)
            except:
                return response.http_400("데이터 에러")

            serializer.save()

            result = {"score": score, "rate": rate}
            return response.http_200(result)

        else:
            return response.http_400(serializer.errors)
