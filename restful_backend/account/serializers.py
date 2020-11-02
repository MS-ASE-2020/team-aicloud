from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import serializers
from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = models.User
        db_table = 't_user'
        fields = ['username', 'email', 'password']
        