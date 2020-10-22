from rest_framework import serializers
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['name', 'time_created']
        read_only_fields = ['time_created']
