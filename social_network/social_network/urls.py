from django.conf import settings
from django.conf.urls import url
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Social Network API",
        default_version="v1",
        description="Rest API Documentation for Social Network",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r"^api/account/", include("account.urls")),
    url(r"^api/feed/", include("feed.urls")),
]

if settings.ENABLE_SWAGGER:
    urlpatterns += [
        url(
            r"^api/swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        url(
            r"^api/swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
