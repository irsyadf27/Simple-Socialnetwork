from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated


<<<<<<< HEAD:socialnetwork/feed/views.py
# Create your views here.
=======
from feed.models import FeedComment, FeedLike, FeedPost
from feed.permissions import FeedPermission
from feed.serializers import CommentSerializer, LikeSerializer, PostSerializer


>>>>>>> 5ed21ee85b7c8d5d6d34be958ff19c247ac4c532:social_network/feed/views.py
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        FeedPermission,
    )

    queryset = FeedPost.objects.all()
    serializer_class = PostSerializer

<<<<<<< HEAD:socialnetwork/feed/views.py
=======
    def get_serializer_context(self):
        context = super(PostViewSet, self).get_serializer_context()
        context.update({"creator": self.request.user})
        return context
>>>>>>> 5ed21ee85b7c8d5d6d34be958ff19c247ac4c532:social_network/feed/views.py


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        FeedPermission,
    )

    queryset = FeedComment.objects.all()
    serializer_class = CommentSerializer

<<<<<<< HEAD:socialnetwork/feed/views.py
=======
    def get_serializer_context(self):
        context = super(CommentViewSet, self).get_serializer_context()
        context.update({"creator": self.request.user})
        return context
>>>>>>> 5ed21ee85b7c8d5d6d34be958ff19c247ac4c532:social_network/feed/views.py


class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        FeedPermission,
    )

    queryset = FeedLike.objects.all()
    serializer_class = LikeSerializer
<<<<<<< HEAD:socialnetwork/feed/views.py
    http_method_names = ['post', 'delete']
=======
    http_method_names = ["post", "delete"]
>>>>>>> 5ed21ee85b7c8d5d6d34be958ff19c247ac4c532:social_network/feed/views.py
