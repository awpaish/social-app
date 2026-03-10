from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Post, PostImage, Comment, Follow
from .serializers import PostSerializer, CommentSerializer, UserProfileSerializer, UserSerializer

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
        serializer = PostSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class FeedView(APIView):
    permission_classes = [permissions.AllowAny]  # or IsAuthenticated

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    
class CreateCommentView(APIView):
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # text = request.data.get("text")
        # post = Post.objects.get(pk=pk)

        # comment = Comment.objects.create(post=post, text=text)

        # return Response({"id": comment.id}, status=201)
        #serializer = PostSerializer(data=request.data)
        serializer = PostSerializer(data=request.data, context={"request": request})
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

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        post.likes.add(request.user)
        return Response({"status": "liked"}, status=200)

    
class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        post.likes.remove(request.user)
        return Response({"status": "unliked"}, status=200)

class CreateCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UploadPostImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "No image uploaded"}, status=400)

        PostImage.objects.create(post=post, image=image_file)
        return Response({"status": "image uploaded"}, status=201)
    
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(get_user_model(), id=pk)
        serializer = UserProfileSerializer(user, context={"request": request})
        return Response(serializer.data)

class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        User = get_user_model()
        target = get_object_or_404(User, id=pk)
        user = request.user

        if user == target:
            return Response({"error": "You cannot follow yourself"}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=user,
            following=target
        )

        if not created:
            follow.delete()
            return Response({"status": "unfollowed"})

        return Response({"status": "followed"})
    
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    