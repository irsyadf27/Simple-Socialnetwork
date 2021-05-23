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
        user = Account.objects.create(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            registration_ip_address=self.context["request"].META["REMOTE_ADDR"],
        )

        user.set_password(validated_data.get("password"))
        user.save()

        celery_app.send_task(
            "accounts.tasks.validate_geolocation_holiday",
            kwargs={
                "account_id": user.id,
                "ip_address": user.registration_ip_address,
                "date_joined": user.date_joined,
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
