from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from account.models import Account
from social_network.celery_app import app as celery_app


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token["username"] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Account.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Account.objects.all())],
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "password",
            "confirm_password",
            "email",
            "first_name",
            "last_name",
        )

    def validate(self, value):
        if value.get("password") != value.get("confirm_password"):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return value

    def create(self, validated_data):
        registration_ip_address = self.context["request"].META.get(
            "REMOTE_ADDR"
        )
        user = Account.objects.create(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            registration_ip_address=registration_ip_address
            if registration_ip_address not in settings.LOCAL_IP_ADDRESSES
            else "",
        )

        user.set_password(validated_data.get("password"))
        user.save()

        celery_app.send_task(
            "account.tasks.validate_geolocation_holiday",
            kwargs={
                "account_id": user.id,
                "registration_ip_address": user.registration_ip_address,
                "date_joined": [
                    user.date_joined.year,
                    user.date_joined.month,
                    user.date_joined.day,
                ],
            },
        )

        return user


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "registration_ip_address",
            "country",
            "is_holiday",
        ]
