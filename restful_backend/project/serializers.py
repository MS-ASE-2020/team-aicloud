from rest_framework import serializers
from . import models


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

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Series
        db_table = 't_series'
        fields = '__all__'
        lookup_field = 'id'

class PredictorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Predictor
        db_table = 't_predictor'
        fields = '__all__'
        read_only_fields = ['time_created']
        lookup_field = 'id'