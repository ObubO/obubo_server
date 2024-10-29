from datetime import datetime
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Posts, Comments, PostLikes, CommentLikes


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


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
