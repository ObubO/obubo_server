from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .serializers import PostSerializer, PostDetailSerializer, PostListSerializer, CommentSerializer, PostCommentSerializer
from common import response
from accounts.authentication import JWTAuthentication
from .models import Post, Comment, PostLike, CommentLike


class PostView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        posts_instance = Post.objects.filter().order_by('-created_at')   # 게시글 인스턴스 리스트 조회

        size = request.query_params.get('size', 10)                     # Paginator 설정
        page_num = request.query_params.get('page', 1)
        paginator = Paginator(posts_instance, size)
        post_list = paginator.get_page(page_num)

        post_serializer = PostListSerializer(post_list, many=True)      # 데이터 직렬화

        result = {"posts": post_serializer.data}

        return response.http_200(result)

    def post(self, request):
        user = request.user                                             # 회원 인증 및 User 인스턴스 조회
        post_serializer = PostSerializer(data=request.data)             # 데이터 유효성 검사

        if post_serializer.is_valid(raise_exception=True):
            post_instance = post_serializer.create(post_serializer.validated_data, user)   # 게시글 인스턴스 생성
            post_instance.save()

            return response.HTTP_200


class PostDetailView(APIView):
    def get(self, request, post_id):
        post_instance = get_object_or_404(Post, pk=post_id)          # 게시글 인스턴스 조회
        post_instance.increase_view_count()                          # 조회수 증가
        post_serializer = PostDetailSerializer(post_instance)        # 데이터 직렬화

        comments_instance = Comment.objects.filter(post=post_id, parent=None).order_by('-created_at')    # 댓글 인스턴스 리스트 조회
        comment_serializer = PostCommentSerializer(instance=comments_instance, many=True)                # 데이터 직렬화

        result = {"post": post_serializer.data, "comments": comment_serializer.data}

        return response.http_200(result)

    def put(self, request, post_id):
        post_serializer = PostSerializer(data=request.data)                        # 데이터 유효성 검사

        if post_serializer.is_valid(raise_exception=True):
            post_instance = get_object_or_404(Post, pk=post_id)                    # 게시글 인스턴스 조회
            post_serializer.update(post_instance, post_serializer.validated_data)  # 게시글 인스턴스 수정

            return response.HTTP_200

        else:
            return response.HTTP_400

    def delete(self, request, post_id):
        try:
            post_instance = get_object_or_404(Post, pk=post_id)      # 게시글 인스턴스 조회
            post_instance.delete()                                   # 게시글 인스턴스 삭제

            return response.HTTP_200

        except Exception as e:
            return response.http_400(str(e))


class CommentView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user                                             # 회원 인증 및 User 인스턴스 조회
        comment_serializer = CommentSerializer(data=request.data)       # 데이터 유효성 검사

        if comment_serializer.is_valid(raise_exception=True):
            comment_instance = comment_serializer.create(comment_serializer.validated_data, user)   # 댓글 인스턴스 생성
            comment_instance.save()

            return response.HTTP_200


class CommentDetailView(APIView):
    def get(self, request, comment_id):
        comment_instance = get_object_or_404(Comment, pk=comment_id)        # 댓글 인스턴스 조회
        comment_serializer = CommentSerializer(comment_instance)            # 데이터 직렬화

        return response.http_200(comment_serializer.data)

    def put(self, request, comment_id):
        comment_serializer = CommentSerializer(data=request.data)           # 데이터 유효성 검사

        if comment_serializer.is_valid(raise_exception=True):
            comment_instance = get_object_or_404(Comment, pk=comment_id)                     # 댓글 인스턴스 조회
            comment_serializer.update(comment_instance, comment_serializer.validated_data)   # 댓글 인스턴스 수정

            return response.HTTP_200

    def delete(self, request, comment_id):
        comment_instance = get_object_or_404(Comment, pk=comment_id)        # 댓글 인스턴스 조회
        comment_instance.delete()                                           # 댓글 인스턴스 삭제

        return response.HTTP_200


class PostLikeView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, post_id):
        user = request.user                                             # 회원 인증 및 User 인스턴스 조회
        post_instance = get_object_or_404(Post, pk=post_id)             # 게시글 인스턴스 조회

        post_like, created = PostLike.objects.get_or_create(user=user, post=post_instance)   # 게시글좋아요 인스턴스 조회 or 생성

        if not created:
            post_like.delete()
            return response.http_200("좋아요 삭제")
        else:
            post_instance.like.add(user)
            return response.http_200("좋아요 추가")


class CommentLikeView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, comment_id):
        user = request.user                                             # 회원 인증 및 User 인스턴스 조회
        comment_instance = get_object_or_404(Comment, pk=comment_id)    # 댓글 인스턴스 조회

        comment_like, created = CommentLike.objects.get_or_create(user=user, comment=comment_instance)   # 댓글좋아요 인스턴스 조회 or 생성

        if not created:
            comment_like.delete()
            return response.http_200("좋아요 삭제")
        else:
            comment_instance.like.add(user)
            return response.http_200("좋아요 추가")

