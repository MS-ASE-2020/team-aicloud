from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from . import models, serializers

# Create your views here.
class UserList(generics.ListCreateAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return models.User.objects.all()

    def perform_create(self, serializer):
        pwd = make_password(self.request.data['password'])
        serializer.save(password=pwd)
