from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import CareGradeExSerializer, CareGradeSimpleSerializer, CareGradeDetailSerializer
from .analysis import AnalysisDiagram, SimpleAnalysisDiagram
from common import response
from accounts import jwt_handler
from accounts.models import User


class CareGradeExAPI(APIView):
    def post(self, request):
        serializer = CareGradeExSerializer(data=request.data)       # 데이터 유효성 검사 및 저장
        if serializer.is_valid():
            serializer.save()

            try:
                data = serializer.validated_data["data"]        # 등급평가 데이터 분석 및 저장
                analysis = SimpleAnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)

                result = {"score": score, "rate": rate}

            except Exception as e:
                return response.http_400(str(e))

            return response.http_200(result)

        else:
            return response.http_400(serializer.errors)


class CareGradeSimpleAPI(APIView):
    def post(self, request):
        access_token = request.headers.get('Authorization', None)
        payload = jwt_handler.decode_token(access_token)                # 토큰 복호화
        user = get_object_or_404(User, pk=payload.get('user_id'))       # User 객체 조회

        serializer = CareGradeSimpleSerializer(data=request.data)       # 데이터 유효성 검사 및 저장
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data, user)
            instance.save()

            try:
                data = serializer.validated_data["data"]        # 등급평가 데이터 분석 및 저장
                analysis = SimpleAnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)

                result = {"score": score, "rate": rate}

                return response.http_200(result)

            except Exception as e:
                return response.http_400(str(e))

        else:
            return response.http_400(serializer.errors)


class CareGradeDetailAPI(APIView):
    def post(self, request):
        access_token = request.headers.get('Authorization', None)       # 토큰 정보 조회
        payload = jwt_handler.decode_token(access_token)                # 토큰 decode
        user = get_object_or_404(User, pk=payload.get('user_id'))       # User 객체 조회

        serializer = CareGradeDetailSerializer(data=request.data)       # 데이터 유효성 검사 및 저장
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data, user)
            instance.save()

            try:
                data = serializer.validated_data['data']        # 등급평가 데이터 분석 및 저장
                analysis = AnalysisDiagram()
                analysis.save(data)
                score = analysis.get_score()
                rate = analysis.get_rate(score)

                result = {"score": score, "rate": rate}

                return response.http_200(result)

            except Exception as e:
                return response.http_400(str(e))

        else:
            return response.http_400(serializer.errors)
