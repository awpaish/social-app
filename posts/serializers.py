from rest_framework import serializers
from .models import Post, PostImage, Comment

class PostImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostImage
        fields = ["post", "image"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "created_at"]

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        #fields = ["id", "user", "text", "created_at", "images"]
        fields = ["id", "text", "created_at", "images", "comments", "like_count"]
        #read_only_fields = ["user", "created_at"]

    def get_like_count(self, obj):
        return obj.likes.count()


#class PostImageSerializer(serializers.ModelSerializer):
#    image_url = serializers.SerializerMethodField()

#    class Meta:
#        model = PostImage
#        fields = ['id', 'image_url']

#    def get_image_url(self, obj):
#        request = self.context.get('request')
#        return request.build_absolute_uri(obj.image.url)
    
    