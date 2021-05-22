from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, LikeViewSet


router = routers.DefaultRouter()
router.register(r"feed", PostViewSet, basename="feeds")
router.register(r"comment", CommentViewSet, basename="comments")
router.register(r"like", LikeViewSet, basename="likes")

urlpatterns = [
    path("", include(router.urls)),
]