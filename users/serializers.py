from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["url", "id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
