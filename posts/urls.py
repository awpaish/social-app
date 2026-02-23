from django.urls import path
#from .views import PostCreateView, PostImageUploadView, PostDetailView, FeedView, CreatePostView
from .views import FeedView, CreatePostView, PostDetailView, CreateCommentView

urlpatterns = [
    #path("create/", PostCreateView.as_view(), name="post-create"),
    #path("upload-image/", PostImageUploadView.as_view(), name="post-image-upload"),
    #path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    #path("feed/", FeedView.as_view(), name="feed"),
    #path("create/", CreatePostView.as_view()),
    path("feed/", FeedView.as_view()),
    path("create/", CreatePostView.as_view()),
    path("<int:pk>/", PostDetailView.as_view()),
    path("<int:pk>/comment/", CreateCommentView.as_view()),

]
