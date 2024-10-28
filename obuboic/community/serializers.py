from datetime import datetime
from rest_framework import serializers
from .models import Posts, Comments, PostLikes, CommentLikes


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
