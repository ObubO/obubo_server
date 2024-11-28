from datetime import datetime
from rest_framework import serializers
from .models import Post, Comment, PostLike, CommentLike


class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='author.member.nickname', read_only=True)
    type = serializers.CharField(source='author.member.member_type.type_name', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'nickname', 'type', 'content', 'created_at', 'likes_count', 'parent', 'replies']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        instance = Comment.objects.create(
            content=validated_data['content'],
            post=validated_data['post'],
            author=validated_data['author'],
            parent=validated_data['parent']
        )

        return instance

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']


class CommentPostSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='author.member.nickname', read_only=True)
    type = serializers.CharField(source='author.member.member_type.type_name', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    class Meta:
        model = Comment
        fields = ['id', 'author', 'nickname', 'type', 'content', 'created_at',
                  'likes_count', 'parent', 'replies']


class CommentLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['comment']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'views', 'created_at', 'updated_at']

    def create(self, validated_data):
        instance = Post.objects.create(
            author=validated_data['author'],
            title=validated_data['title'],
            content=validated_data['content'],
        )

        return instance


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']


class PostLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post']


class PostListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='author.member.nickname')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'nickname', 'views', 'created_at', 'comments_count', 'likes_count']


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.member.nickname', read_only=True)
    author_type = serializers.CharField(source='author.member.member_type.type_name', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'author_type', 'title', 'content', 'views', 'created_at',
                  'comments_count', 'likes_count']
        read_only_fields = ['id', 'created_at', 'updated_at']
