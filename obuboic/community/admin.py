from django.contrib import admin

from .models import Category, Post, Comment, PostLike, CommentLike


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)      # 관리자 리스트 페이지에서 보여줄 컬럼
    search_fields = ("name",)           # 상단 검색창으로 검색할 필드
    ordering = ("order", "id")          # 정렬 기준 (order, id 순)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'order')
        }),
        ('시스템 정보', {
            'fields': ('is_active', 'created_at',)
        }),
    )


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', )
    search_fiedls = ('author', 'title')
    ordering = ('-created_at',)
    readonly_fields = ['created_at', 'updated_at', ]
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'author', 'content')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'post', 'author',)
    search_fiedls = ('author', 'post')
    ordering = ('-created_at',)
    readonly_fields = ['parent', 'created_at', 'updated_at']
    fieldsets = (
        ('기본 정보', {
            'fields': ('post', 'author', 'content')
        }),
        ('시스템 정보', {
            'fields': ('parent', 'created_at', 'updated_at')
        }),
    )


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    fields = ['user', 'post']
    list_display = ['id', 'user', 'post']


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    fields = ['user', 'comment']
    list_display = ['id', 'user', 'comment']
