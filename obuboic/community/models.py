from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=10)

    objects = models.Manager()

    class Meta:
        verbose_name = "게시판 카테고리"

    def __str__(self):
        return self.category_name


class Posts(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="posts")
    title = models.CharField(_("title"), max_length=100)
    content = models.TextField(_("content"))
    like = models.ManyToManyField(User, through="PostLike", through_fields=("post", "user"), related_name="like_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "게시글"

    def __str__(self):
        return self.title


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    content = models.TextField(_("content"))
    like = models.ManyToManyField(User, through="CommentLike", through_fields=("comment", "user"), related_name="like_comments")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "댓글"

    def __str__(self):
        return self.content


class PostLike(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = "게시글 좋아요"
        unique_together = ('user', 'post')


class CommentLike(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = "댓글 좋아요"
        unique_together = ('user', 'comment')

