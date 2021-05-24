from http import HTTPStatus

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from feed.models import FeedComment, FeedLike, FeedPost
from feed.permissions import FeedPermission
from feed.serializers import CommentSerializer, LikeSerializer, PostSerializer


class FeedPostViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        FeedPermission,
    )

    queryset = FeedPost.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        if "pk" in self.kwargs:
            context["post"] = self.get_object()

        return context

    @action(
        detail=True,
        methods=["post"],
        serializer_class=CommentSerializer,
        permission_classes=[
            IsAuthenticated,
        ],
        url_path="comments/add",
    )
    def add_comment(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], serializer_class=CommentSerializer)
    def comments(self, request, *args, **kwargs):
        queryset = FeedComment.objects.filter(post=self.get_object())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=LikeSerializer,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def like(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(post=self.get_object())
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def unlike(self, request, *args, **kwargs):
        FeedLike.objects.filter(
            post=self.get_object(), creator=request.user
        ).delete()
        return Response(status=HTTPStatus.NO_CONTENT)
