from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import CareGradeExSerializer, CareGradeSimpleSerializer, UserCareDetailSerializer
from .analysis import AnalysisDiagram, SimpleAnalysisDiagram
from common import response
from accounts import views as account
from accounts import models


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

                result = {"score": score, "rate": rate}
            except:
                return response.http_400("데이터 에러")

            # 간소평가 등록
            serializer.save()

            return response.http_200(result)

        else:
            return response.http_400(serializer.errors)


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


class CareGradeDetailAPI(APIView):
    def post(self, request):
        # User 정보 조회
        access_token = request.headers.get('Authorization', None)
        jwt_decode_data = account.jwt_decode_handler(access_token)
        jwt_is_valid, user = jwt_decode_data[0], jwt_decode_data[1]

        if not jwt_is_valid:
            result = jwt_decode_data[1]
            return response.http_400(result)

        # 등급평가 데이터 유효성 검사
        care_serializer = UserCareDetailSerializer(data=request.data)
        if care_serializer.is_valid():
            data = care_serializer.validated_data['data']

            # 등급평가 분석
            try:
                analysis = AnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)
                result = {"score": score, "rate": rate}
            except:
                return response.http_400("데이터 에러")

            # 등급평가 정보 저장
            care_instance = care_serializer.create(care_serializer.validated_data)
            care_instance.set_user(user)

            care_instance.save()

            return response.http_200(result)

        else:
            return response.http_400(care_serializer.errors)
