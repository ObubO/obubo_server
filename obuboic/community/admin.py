from django.contrib import admin

from .models import Post, Comment, PostLike, CommentLike


# Register your models here.
class PostsAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'content', 'created_at', 'updated_at']
    list_display = ('id', 'title', 'author', )

    readonly_fields = ['created_at', 'updated_at', ]

    search_fiedls = ('author', 'title')
    ordering = ('-created_at', )


class CommentsAdmin(admin.ModelAdmin):
    fields = ['id', 'post', 'author', 'content', 'created_at', 'parent']
    list_display = ('id', 'content', 'post', 'author',)

    readonly_fields = ['id', 'created_at', 'parent']

    search_fiedls = ('author', 'post')
    ordering = ('-created_at',)


class PostLikeAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'post']
    list_display = ['id', 'user', 'post']


class CommentLikeAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'comment']
    list_display = ['id', 'user', 'comment']


admin.site.register(Post, PostsAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
