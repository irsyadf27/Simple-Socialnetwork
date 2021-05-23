from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


from account.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    AccountSerializer,
)
from account.models import Account


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = Account.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class AccountDetailDetail(APIView):
    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)
