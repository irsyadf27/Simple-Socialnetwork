from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated


from feed.models import FeedComment, FeedLike, FeedPost
from feed.permissions import FeedPermission
from feed.serializers import CommentSerializer, LikeSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        FeedPermission,
    )

    queryset = FeedPost.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({"creator": self.request.user})
        return context


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        FeedPermission,
    )

    queryset = FeedComment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super(CommentViewSet, self).get_serializer_context()
        context.update({"creator": self.request.user})
        return context


class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        FeedPermission,
    )

    queryset = FeedLike.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ["post", "delete"]
