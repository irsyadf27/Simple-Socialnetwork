from django.urls import path, include
from rest_framework import routers


from feed.views import FeedPostViewSet


router = routers.DefaultRouter()
router.register(r"", FeedPostViewSet, basename="feeds")

urlpatterns = [
    path("", include(router.urls)),
]
