from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers


# Create your views here.
class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return self.request.user.projects.all()

    def perform_create(self, serializer):
        serializer.save(related_user=self.request.user)
