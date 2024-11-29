from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .serializers import PostSerializer, CommentSerializer, CommentGroupSerializer, PostListSerializer, PostDetailSerializer
from common import response
from accougints.jwt_handler import decode_token
from accounts.models import User
from .models import Post, Comment, PostLike, CommentLike


class PostView(APIView):
    def get(self, request):
        size = request.query_params.get('size', 10)
        page_num = request.query_params.get('page', 1)

        post_list = Post.objects.filter().order_by('-created_at')  # 게시글 최신순 조회
        paginator = Paginator(post_list, size)                        # Paginator 설정
        posts = paginator.get_page(page_num)

        serializer = PostListSerializer(posts, many=True)               # 게시글 리스트 serializer
        result = {"posts": serializer.data}

        return response.http_200(result)

    def post(self, request):
        access_token = request.headers.get('Authorization', None)  # 토큰 조회

        # 토큰 decoding
        try:
            payload = decode_token(access_token)  # 토큰 decoding
            user = get_object_or_404(User, pk=payload.get('user_id'))
        except Exception as e:
            return response.http_400(str(e))

        request_data = request.POST.copy()                      # request.data를 가공하기 위한 복사본 생성
        request_data['author'] = user.pk                        # request.data에 헤더로 넘어온 회원 데이터 추가

        serializer = PostSerializer(data=request_data)          # 요청 데이터 serialize

        if serializer.is_valid(raise_exception=True):           # 요청 데이터 유효성 검사
            serializer.save()                                   # post 인스턴스 생성

            return response.HTTP_200


class PostDetailView(APIView):
    # 게시글 상세 조회
    def get(self, request, post_id):
        instance = get_object_or_404(Post, pk=post_id)          # 게시글 인스턴스 조회
        instance.views += 1
        instance.save()
        serializer = PostDetailSerializer(instance)             # 조회된 인스턴스 serialize
        result = {"posts": serializer.data}

        return response.http_200(result)

    # 게시글 수정
    def put(self, request, post_id):
        serializer = PostSerializer(data=request.data)              # 요청 데이터 직렬화

        if serializer.is_valid(raise_exception=True):                                   # 요청 데이터 유효성 검사
            instance = get_object_or_404(Post, pk=post_id)          # post 인스턴스 조회
            serializer.update(instance, serializer.validated_data)  # 인스턴스 수정

            return response.HTTP_200

        else:
            return response.HTTP_400

    def delete(self, request, post_id):
        try:
            instance = get_object_or_404(Post, pk=post_id)  # post 인스턴스 조회
            instance.delete()                                # 인스턴스 삭제

            return response.HTTP_200

        except:
            return response.HTTP_400


class CommentView(APIView):
    # (게시글 당) 댓글 리스트 조회
    def get(self, request, post_id):
        comment_list = Comment.objects.filter(post=post_id, parent=None).order_by('-created_at')  # 댓글 최신순 조회
        serializer = CommentGroupSerializer(instance=comment_list, many=True)
        result = {"comments": serializer.data}
        return response.http_200(result)

    # 댓글 생성
    def post(self, request):
        access_token = request.headers.get('Authorization', None)  # 토큰 조회

        # 토큰 decoding
        try:
            payload = decode_token(access_token)              # 토큰 decoding
            user = get_object_or_404(User, pk=payload.get('user_id'))
        except Exception as e:
            return response.http_400(str(e))

        request_data = request.POST.copy()                      # request.data를 가공하기 위한 복사본 생성
        request_data['author'] = user.pk                        # request.data에 헤더로 넘어온 회원 데이터 추가

        serializer = CommentSerializer(data=request_data)       # 요청 데이터 serialize

        if serializer.is_valid(raise_exception=True):           # 요청 데이터 유효성 검사
            serializer.save()                                   # comment 인스턴스 생성

            return response.HTTP_200


class CommentDetailView(APIView):
    def get(self, request, comment_id):
        instance = get_object_or_404(Comment, pk=comment_id)       # 댓글 인스턴스 조회
        serializer = CommentSerializer(instance)                    # 조회된 인스턴스 serialize

        return response.http_200(serializer.data)

    def put(self, request, comment_id):
        serializer = CommentSerializer(data=request.data)           # 요청 데이터 serialize

        if serializer.is_valid():                                   # 요청 데이터 유효성 검사
            instance = get_object_or_404(Comment, pk=comment_id)   # comment 인스턴스 조회
            serializer.update(instance, serializer.validated_data)  # 인스턴스 수정

            return response.HTTP_200

    def delete(self, request, comment_id):
        instance = get_object_or_404(Comment, pk=comment_id)
        instance.delete()

        return response.HTTP_200


class PostLikeView(APIView):
    def post(self, request, post_id):
        access_token = request.headers.get('Authorization', None)  # 토큰 조회
        post = get_object_or_404(Post, pk=post_id)

        # 토큰 decoding
        try:
            payload = decode_token(access_token)  # 토큰 decoding
            user = get_object_or_404(User, pk=payload.get('user_id'))
        except Exception as e:
            return response.http_400(str(e))

        post_like, created = PostLike.objects.get_or_create(user=user, post=post)

        if not created:
            post_like.delete()
            return response.http_200("좋아요 삭제")
        else:
            post.like.add(user)
            return response.http_200("좋아요 추가")


class CommentLikeView(APIView):
    def post(self, request, comment_id):
        access_token = request.headers.get('Authorization', None)  # 토큰 조회
        comment = get_object_or_404(Comment, pk=comment_id)

        # 토큰 decoding
        try:
            payload = decode_token(access_token)  # 토큰 decoding
            user = get_object_or_404(User, pk=payload.get('user_id'))
        except Exception as e:
            return response.http_400(str(e))

        comment_like, created = CommentLike.objects.get_or_create(user=user, comment=comment)

        if not created:
            comment_like.delete()
            return response.http_200("좋아요 삭제")
        else:
            comment.like.add(user)
            return response.http_200("좋아요 추가")

