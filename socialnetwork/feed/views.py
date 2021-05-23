from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import FeedPost, FeedComment, FeedLike
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import FeedPermission


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, FeedPermission,)

    queryset = FeedPost.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, FeedPermission,)

    queryset = FeedComment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, FeedPermission,)

    queryset = FeedLike.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ['post', 'delete']
