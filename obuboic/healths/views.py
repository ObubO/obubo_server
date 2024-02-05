from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CareGradeSerializer
from .analysis import AnalysisDiagram


# Create your views here.
class CareGradeAPI(APIView):
    def get(self, request):
        serializer = CareGradeSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data["data"]

            # 간소평가 분석
            analysis = AnalysisDiagram()
            analysis.save(data)
            score = analysis.clean_diagram() + analysis.bath_diagram() + analysis.eat_diagram() \
                + analysis.assist_diagram() + analysis.behav_diagram() + analysis.support_diagram() \
                + analysis.nurse_diagram() + analysis.rehab_diagram()
            result = analysis.get_rate(score)

            # 간소평가 등록
            serializer.save()
            res = Response(
                {
                    "code": 200,
                    "message": "평가결과 등록 완료",
                    "result": result,
                },
                status=status.HTTP_200_OK,
            )
            return res

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




