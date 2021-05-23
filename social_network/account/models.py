from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given parameters.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given parameters.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    registration_ip_address = models.GenericIPAddressField(
        blank=True, null=True
    )
    country = models.CharField(max_length=50, blank=True, null=True)
    is_holiday = models.BooleanField(default=False)

    objects = MyUserManager()

    def __str__(self):
        return self.username
