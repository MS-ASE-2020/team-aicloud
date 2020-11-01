from rest_framework import serializers
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        db_table = 't_project'
        fields = ['name', 'time_created']
        read_only_fields = ['time_created']

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dataset
        db_table = 't_data'
        fields = ['name', 'uuid', 'time_created', 'upload']
        read_only_fields = ['time_created', 'uuid']
