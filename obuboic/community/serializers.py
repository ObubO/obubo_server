from datetime import datetime
from rest_framework import serializers
from .models import Post, Comment, PostLike, CommentLike


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'likes_count']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        instance = Comment.objects.create(
            content=validated_data['content'],
            post=validated_data['post'],
            author=validated_data['author']
        )

        return instance


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentPostSerializer(many=True, default=[])
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comments_count', 'likes_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

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


class CommentLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['comment']
