from http import HTTPStatus
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=True, methods=["get"])
    def comments(self, request, *args, **kwargs):
        queryset = FeedComment.objects.filter(post=kwargs.get("pk"))

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], serializer_class=None)
    def like(self, request, *args, **kwargs):
        request.data["post"] = kwargs.get("pk")
        serializer = LikeSerializer(data=request.data, context={"post": kwargs.get("pk"), "request": self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], serializer_class=None)
    def unlike(self, request, *args, **kwargs):
        FeedLike.objects.filter(
            post_id=kwargs.get("pk"), creator=request.user
        ).delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        FeedPermission,
    )

    queryset = FeedComment.objects.all()
    serializer_class = CommentSerializer