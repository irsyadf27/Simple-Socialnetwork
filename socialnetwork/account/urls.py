from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyObtainTokenPairView, RegisterView, AccountDetailDetail

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('detail/<int:pk>/', AccountDetailDetail.as_view()),
]