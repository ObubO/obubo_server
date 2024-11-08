from datetime import datetime
from rest_framework import serializers
from .models import Posts, Comments, PostLike, CommentLike


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'post', 'author', 'content', 'created_at', 'likes_count']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        instance = Comments.objects.create(
            content=validated_data['content'],
            post=validated_data['post'],
            author=validated_data['author']
        )

        return instance


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'content']


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'author', 'content', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentPostSerializer(many=True, source='comments_set', default=[])
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Posts
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'likes_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        instance = Posts.objects.create(
            author=validated_data['author'],
            title=validated_data['title'],
            content=validated_data['content'],
        )

        return instance


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'title']


class PostLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post']


class CommentLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['comment']
