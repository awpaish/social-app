from rest_framework import serializers
from .models import Post, PostImage, Comment
from django.contrib.auth import get_user_model


class PostImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostImage
        #fields = ["post", "image"]
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        #fields = ["id", "text", "created_at"]
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    liked_by_user = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        #fields = ["id", "user", "text", "created_at", "images"]
        #fields = ["id", "text", "created_at", "images", "comments", "like_count"]
        #read_only_fields = ["user", "created_at"]
        fields = "__all__"

    def get_liked_by_user(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj.likes.filter(id=user.id).exists()

    def get_like_count(self, obj):
        return obj.likes.count()

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "post"]

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "image"]

User = get_user_model()

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
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]




# class LikeSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Like
#         fields = "__all__"

#class PostImageSerializer(serializers.ModelSerializer):
#    image_url = serializers.SerializerMethodField()

#    class Meta:
#        model = PostImage
#        fields = ['id', 'image_url']

#    def get_image_url(self, obj):
#        request = self.context.get('request')
#        return request.build_absolute_uri(obj.image.url)
    
    