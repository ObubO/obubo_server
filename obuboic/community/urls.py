from django.urls import path
from . import views

urlpatterns = [
    # 게시글
    path('posts', views.PostView.as_view()),                            # GET: 게시글 목록 조회 / POST: 게시글 생성
    path('posts/<int:post_id>', views.PostDetailView.as_view()),        # GET: 게시글 상세 조회 / PATCH: 게시글 수정 / DELETE: 게시글 삭제
    path('posts/<int:post_id>/like', views.PostLikeView.as_view()),     # POST: 게시글 좋아요

    # 댓글
    path('comments', views.CommentView.as_view()),                              # POST: 댓글 생성
    path('comments/<int:comment_id>', views.CommentDetailView.as_view()),       # PATCH: 댓글 수정 / DELETE: 댓글 삭제
    path('comments/<int:comment_id>/like', views.CommentLikeView.as_view()),    # POST: 댓글 좋아요

]

