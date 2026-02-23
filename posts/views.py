from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Post, PostImage, Comment, Like
from .serializers import PostSerializer

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    
class CreatePostView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        text = request.data.get("text")
        images = request.FILES.getlist("images")

        post = Post.objects.create(text=text)

        for img in images:
            PostImage.objects.create(post=post, image=img)

        return Response({"id": post.id}, status=201)
    
class CreateCommentView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        text = request.data.get("text")
        post = Post.objects.get(pk=pk)

        comment = Comment.objects.create(post=post, text=text)

        return Response({"id": comment.id}, status=201)
    

class LikePostView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        Like.objects.create(post=post)
        return Response({"status": "liked"}, status=201)


class UnlikePostView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        Like.objects.filter(post=post).first().delete()
        if Like:
            Like.delete()

        return Response({"status": "unliked"}, status=200)
    