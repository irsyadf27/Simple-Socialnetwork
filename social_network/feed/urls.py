from django.urls import path, include
from rest_framework import routers


from feed.views import PostViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register(r"feed", PostViewSet, basename="feeds")
router.register(r"comment", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(router.urls)),
]
