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
    title = models.CharField(_("title"), max_length=20)
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "게시글"

    def __str__(self):
        return self.title


class Comments(models.Model):
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "댓글"

    def __str__(self):
        return self.content


class PostLikes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = "게시글 공감"

    def __str__(self):
        return self.user.username


class CommentLikes(models.Model):
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        verbose_name = "댓글 공감"

    def __str__(self):
        return self.user.username

