from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from .managers import CustomUserManager


# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}, {self.username}"

    @staticmethod
    def get_user_by_token(request):
        return Token.objects.get(key=request.META["HTTP_TOKEN"]).user
