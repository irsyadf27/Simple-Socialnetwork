from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


from account.models import Account
from account.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    AccountSerializer,
)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def get_serializer_context(self):
        context = super(RegisterView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class AccountDetailDetail(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
