from rest_framework import serializers
from .models import Post, Comment


class AuthorSafeMixin(serializers.Serializer):
    author = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    def get_author(self, obj):
        if obj.user:
            return obj.user.user_profiles.nickname
        else:
            return None

    def get_user_type(self, obj):
        if obj.user:
            return obj.user.user_profiles.user_type
        else:
            return None


class CommentSerializer(AuthorSafeMixin, serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data, user=None):
        instance = Comment(
            user=user,
            **validated_data
        )

        return instance


# -- 하나의 게시글에 달린 댓글 조회(대댓글 포함) -- #
class PostCommentSerializer(AuthorSafeMixin, serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='like.count', read_only=True)
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'user',
            'content', 'like_count', 'replies',
            'created_at'
        ]


class PostSerializer(AuthorSafeMixin, serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data, user=None):
        instance = Post.objects.create(
            user=user,
            **validated_data
        )

        return instance


class PostDetailSerializer(AuthorSafeMixin, serializers.ModelSerializer):
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='like.count', read_only=True)
    user_type = serializers.CharField(source='user.user_profiles.user_type')

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'user_type',
            'title', 'content', 'views',
            'comment_count', 'like_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = fields


class PostListSerializer(AuthorSafeMixin, serializers.ModelSerializer):
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'author', 'views',
            'comment_count', 'like_count',
            'created_at'
        ]
