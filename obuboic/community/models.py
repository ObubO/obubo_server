from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(verbose_name="카테고리명", max_length=20)
    order = models.PositiveIntegerField(verbose_name="노출 순서", default=0)
    is_active = models.BooleanField(verbose_name="사용 여부", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_category'
        verbose_name = "게시판 카테고리"
        verbose_name_plural = "게시판 카테고리 목록"

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_posts")
    like = models.ManyToManyField(User, through="PostLike", through_fields=("post", "user"), related_name="like_posts")

    title = models.CharField(verbose_name="제목", max_length=100)
    content = models.TextField(verbose_name="내용")
    views = models.PositiveIntegerField(verbose_name="조회수", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'post'
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"

    def __str__(self):
        return self.title

    def increase_view_count(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_comments")
    like = models.ManyToManyField(User, through="CommentLike", through_fields=("comment", "user"),
                                  related_name="like_comments")

    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'comment'
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"

    def __str__(self):
        return self.content[:20]


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'post_like'
        verbose_name = "게시글 좋아요"
        verbose_name_plural = "게시글 좋아요 목록"
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} - {self.post}"


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'comment_like'
        verbose_name = "댓글 좋아요"
        verbose_name_plural = "댓글 좋아요 목록"
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user} - {self.comment}"


