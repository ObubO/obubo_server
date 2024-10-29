from datetime import datetime
from rest_framework import serializers
from .models import Posts, Comments, PostLikes, CommentLikes


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        instance = Posts.objects.create(
            author=validated_data['author'],
            title=validated_data['title'],
            content=validated_data['content'],
        )

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        instance = Comments.objects.create(
            content=validated_data['content'],
            post=validated_data['post'],
            author=validated_data['author']
        )

        return instance
