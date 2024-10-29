from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .serializers import PostSerializer, CommentSerializer
from common import response
from accounts.views import jwt_decode_handler
from .models import Posts, Comments


class PostView(APIView):
    def get(self, request):
        post_list = Posts.objects.filter().order_by('-created_at')  # 게시글 최신순 조회

        paginator = Paginator(post_list, 10)                        # Paginator 설정
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        serializer = PostSerializer(posts, many=True)               # 게시글 리스트 serializer

        return response.http_200(serializer.data)

    def post(self, request):
        access_token = request.headers.get('Authorization', None)       # 토큰 조회
        jwt_decode_data = jwt_decode_handler(access_token)              # 토큰 decoding
        jwt_is_valid, user = jwt_decode_data[0], jwt_decode_data[1]     # 회원 정보 조회

        if not jwt_is_valid:
            return response.HTTP_400

        try:
            request_data = request.POST.copy()                      # request.data를 가공하기 위한 복사본 생성
            request_data['author'] = user.pk                        # request.data에 헤더로 넘어온 회원 데이터 추가

            serializer = PostSerializer(data=request_data)          # 요청 데이터 serialize

            if serializer.is_valid():                               # 요청 데이터 유효성 검사
                serializer.create(serializer.validated_data)        # post 인스턴스 생성

                return response.HTTP_200
            else:
                return response.http_400(serializer.errors)

        except:
            return response.http_500("서버 에러")


class PostDetailView(APIView):
    def get(self, request, post_id):
        instance = get_object_or_404(Posts, pk=post_id)     # 게시글 인스턴스 조회
        serializer = PostSerializer(instance)               # 조회된 인스턴스 serialize

        return response.http_200(serializer.data)

    def put(self, request, post_id):
        serializer = PostSerializer(data=request.data)              # 요청 데이터 직렬화

        if serializer.is_valid():                                   # 요청 데이터 유효성 검사
            instance = get_object_or_404(Posts, pk=post_id)         # post 인스턴스 조회
            serializer.update(instance, serializer.validated_data)  # 인스턴스 수정

            return response.HTTP_200

        else:
            return response.HTTP_400

    def delete(self, request, post_id):
        try:
            instance = get_object_or_404(Posts, pk=post_id)  # post 인스턴스 조회
            instance.delete()                                # 인스턴스 삭제

            return response.HTTP_200

        except:
            return response.HTTP_400


class CommentView(APIView):
    def post(self, request):
        access_token = request.headers.get('Authorization', None)       # 토큰 조회
        jwt_decode_data = jwt_decode_handler(access_token)              # 토큰 decoding / jwt_decode_handler의 return 값을 user.pk로 주면 코드 최적화 가능
        jwt_is_valid, user = jwt_decode_data[0], jwt_decode_data[1]     # 회원 정보 조회

        if not jwt_is_valid:                                            # 토큰 유효성 검사
            return response.HTTP_400

        try:
            request_data = request.POST.copy()                      # request.data를 가공하기 위한 복사본 생성
            request_data['author'] = user.pk                        # request.data에 헤더로 넘어온 회원 데이터 추가

            serializer = CommentSerializer(data=request_data)       # 요청 데이터 serialize

            if serializer.is_valid():                               # 요청 데이터 유효성 검사
                serializer.create(serializer.validated_data)        # comment 인스턴스 생성

                return response.HTTP_200

            else:
                return response.HTTP_400

        except:
            return response.HTTP_400


class CommentDetailView(APIView):
    def get(self, request, comment_id):
        instance = get_object_or_404(Comments, pk=comment_id)       # 댓글 인스턴스 조회
        serializer = CommentSerializer(instance)                    # 조회된 인스턴스 serialize

        return response.http_200(serializer.data)

    def put(self, request, comment_id):
        serializer = CommentSerializer(data=request.data)           # 요청 데이터 serialize

        if serializer.is_valid():                                   # 요청 데이터 유효성 검사
            instance = get_object_or_404(Comments, pk=comment_id)   # comment 인스턴스 조회
            serializer.update(instance, serializer.validated_data)  # 인스턴스 수정

            return response.HTTP_200

    def delete(self, request, comment_id):
        instance = get_object_or_404(Comments, pk=comment_id)
        instance.delete()

        return response.HTTP_200

