from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.PostView.as_view()),
    path('posts/<int:post_id>', views.PostDetailView.as_view()),
    path('posts/<int:post_id>/like', views.PostLikeView.as_view()),

    path('comments', views.CommentView.as_view()),
    path('comments/<int:comment_id>', views.CommentDetailView.as_view()),
    path('comments/<int:comment_id>/like', views.CommentLikeView.as_view()),

]

