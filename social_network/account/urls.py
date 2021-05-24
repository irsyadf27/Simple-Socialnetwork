from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account.views import (
    MyObtainTokenPairView,
    RegisterView,
    AccountDetailDetail,
)

urlpatterns = [
    path(
        "auth-token/",
        MyObtainTokenPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("<int:pk>/", AccountDetailDetail.as_view()),
]
