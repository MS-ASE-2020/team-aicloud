from rest_framework import serializers
from . import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        db_table = 't_project'
        fields = '__all__'
        read_only_fields = ['time_created']
        lookup_field = 'id'

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dataset
        db_table = 't_data'
        fields = '__all__'
        read_only_fields = ['time_created', 'uuid']
        lookup_field = 'id'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        db_table = 't_job'
        fields = '__all__'
        read_only_fields = ['time_created']
        lookup_field = 'id'

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        db_table = 't_model'
        fields = '__all__'
        read_only_fields = ['time_created']
        lookup_field = 'id'