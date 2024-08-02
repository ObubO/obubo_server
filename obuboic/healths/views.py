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
            analysis = SimpleAnalysisDiagram()
            analysis.save(data)
            score = analysis.clean_diagram() + analysis.bath_diagram() + analysis.eat_diagram() \
                + analysis.assist_diagram() + analysis.behav_diagram() + analysis.support_diagram() \
                + analysis.nurse_diagram() + analysis.rehab_diagram()
            rate = analysis.get_rate(score)

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
            analysis = SimpleAnalysisDiagram()
            analysis.save(data)
            score = analysis.clean_diagram() + analysis.bath_diagram() + analysis.eat_diagram() \
                + analysis.assist_diagram() + analysis.behav_diagram() + analysis.support_diagram() \
                + analysis.nurse_diagram() + analysis.rehab_diagram()
            rate = analysis.get_rate(score)

            # 간소평가 등록
            serializer.save()
            res = Response(
                {
                    "success": True,
                    "result": {
                        "score": score,
                        "rate": rate,
                    }
                },
                status=status.HTTP_200_OK,
            )
            return res

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class CareGradeDetailAPI(APIView):
    def post(self, request):
        serializer = CareGradeDetailSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data["data"]

            # 요양등급평가 분석
            analysis = AnalysisDiagram()
            analysis.save(data)
            score = analysis.clean_diagram() + analysis.bath_diagram() + analysis.eat_diagram() \
                + analysis.assist_diagram() + analysis.behav_diagram() + analysis.support_diagram() \
                + analysis.nurse_diagram() + analysis.rehab_diagram()
            rate = analysis.get_rate(score)

            # 요양등급평가 등록
            serializer.save()
            res = Response(
                {
                    "success": True,
                    "result": {
                        "score": score,
                        "rate": rate,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
