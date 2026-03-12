from rest_framework import serializers
from .models import Post, PostImage, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


# -----------------------------
# Post Images
# -----------------------------
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]


# -----------------------------
# Comments
# -----------------------------
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "post"]


# -----------------------------
# Posts
# -----------------------------
class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["user", "likes", "created_at"]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_liked_by_user(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj.likes.filter(id=user.id).exists()


# -----------------------------
# User Profile
# -----------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True, source="post_set")
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "posts",
            "followers_count",
            "following_count",
            "is_following",
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        user = self.context["request"].user
        return obj.followers.filter(follower=user).exists()


# -----------------------------
# Basic User Serializer
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        