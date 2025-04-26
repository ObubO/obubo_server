from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data, user=None):
        instance = Comment(
            author=user,
            **validated_data
        )

        return instance


# -- 하나의 게시글에 달린 댓글 조회(대댓글 포함) -- #
class PostCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='author.user_profile.nickname', read_only=True)
    user_type = serializers.CharField(source='author.user_profile.user_type.name', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'nickname', 'user_type',
            'content', 'likes_count', 'replies',
            'created_at', 'parent'
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data, user=None):
        instance = Post.objects.create(
            author=user,
            **validated_data
        )

        return instance


class PostDetailSerializer(serializers.ModelSerializer):
    author_type = serializers.CharField(source='author.user_profile.user_type.name', read_only=True)
    nickname = serializers.CharField(source='author.user_profile.nickname', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'nickname', 'author_type',
            'title', 'content', 'views',
            'created_at', 'updated_at',
            'comments_count', 'likes_count'
        ]
        read_only_fields = fields


# -- 게시글 리스트 조회 --#
class PostListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='author.user_profile.nickname')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='like.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'nickname', 'views', 'created_at', 'comments_count', 'likes_count']
