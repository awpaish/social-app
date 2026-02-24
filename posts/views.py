from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
    #parser_classes = [MultiPartParser, FormParser]
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "Use POST to create posts"})

    def post(self, request):
        # text = request.data.get("text")
        # images = request.FILES.getlist("images")

        # post = Post.objects.create(text=text)

        # for img in images:
        #     PostImage.objects.create(post=post, image=img)

        # return Response({"id": post.id}, status=201)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    
class CreateCommentView(APIView):
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # text = request.data.get("text")
        # post = Post.objects.get(pk=pk)

        # comment = Comment.objects.create(post=post, text=text)

        # return Response({"id": comment.id}, status=201)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# class LikePostView(APIView):
#     #permission_classes = [permissions.AllowAny]
#     permission_classes = [permissions.IsAuthenticated]


#     def post(self, request, pk):
#         # post = Post.objects.get(pk=pk)
#         # Like.objects.create(post=post)
#         # return Response({"status": "liked"}, status=201)
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            like.delete()
            return Response({"message": "Unliked"}, status=200)

        return Response({"message": "Liked"}, status=201)
    

class UnlikePostView(APIView):
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, post_id):
        # post = Post.objects.get(pk=pk)
        # Like.objects.filter(post=post).first().delete()
        # if Like:
        #     Like.delete()

        # return Response({"status": "unliked"}, status=200)
        # serializer = PostSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save(user=request.user)
        #     return Response(serializer.data, status=201)
        # return Response(serializer.errors, status=400)
        post = get_object_or_404(Post, id=post_id)

        like = Like.objects.filter(
            user=request.user,
            post=post
        ).first()

        if not like:
            return Response({"message": "You haven't liked this post"}, status=400)

        like.delete()
        return Response({"message": "Unliked"}, status=200)
