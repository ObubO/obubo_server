from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import CareGradeExSerializer, CareGradeSimpleSerializer, CareGradeDetailSerializer, GovServiceSerializer
from .analysis import AnalysisDiagram, SimpleAnalysisDiagram
from common import response
from accounts.authentication import JWTAuthentication


class CareGradeExAPI(APIView):
    def post(self, request):
        serializer = CareGradeExSerializer(data=request.data)

        if serializer.is_valid():       # 데이터 유효성 검사 및 저장
            serializer.save()

            service_queryset = GovServiceSerializer.filter_age_region(self, serializer.validated_data)     # 지원금 조회
            service_serializer = GovServiceSerializer(service_queryset, many=True)

            try:
                data = serializer.validated_data["data"]        # 등급평가 데이터 분석 및 저장
                analysis = SimpleAnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)

                result = {"score": score, "rate": rate, 'service': service_serializer.data}

            except Exception as e:
                return response.http_400(str(e))

            return response.http_200(result)

        else:
            return response.http_400(serializer.errors)


class CareGradeSimpleAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user                                             # 회원 인증 및 User 인스턴스 조회
        print(user)
        serializer = CareGradeSimpleSerializer(data=request.data)       # 데이터 유효성 검사

        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data, user)
            instance.save()

            service_queryset = GovServiceSerializer.filter_age_region(self, serializer.validated_data)  # 지원금 조회
            service_serializer = GovServiceSerializer(service_queryset, many=True)

            try:
                data = serializer.validated_data["data"]        # 등급평가 데이터 분석 및 저장
                analysis = SimpleAnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)

                result = {"score": score, "rate": rate, 'service': service_serializer.data}

                return response.http_200(result)

            except Exception as e:
                return response.http_400(str(e))

        else:
            return response.http_400(serializer.errors)


class CareGradeDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user                                             # 회원 인증 및 User 인스턴스 조회
        serializer = CareGradeDetailSerializer(data=request.data)       # 데이터 유효성 검사

        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data, user)
            instance.save()

            service_queryset = GovServiceSerializer.filter_age_region(self, serializer.validated_data)  # 지원금 조회
            service_serializer = GovServiceSerializer(service_queryset, many=True)

            try:
                data = serializer.validated_data['data']        # 등급평가 데이터 분석 및 저장
                analysis = AnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)

                result = {"score": score, "rate": rate, 'service': service_serializer.data}

                return response.http_200(result)

            except Exception as e:
                return response.http_400(str(e))

        else:
            return response.http_400(serializer.errors)
