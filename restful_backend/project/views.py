from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication, permissions, decorators, viewsets, mixins, status
from rest_framework.decorators import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from . import models
from . import serializers
from .utils import *


# Create your views here.
class ProjectViewSet(
    mixins.CreateModelMixin, # .create(request) for creating a project for the user
    mixins.ListModelMixin, # .list(request) for listing all projects of the user
    mixins.RetrieveModelMixin, # .retrieve(request) for returning a specify project
    viewsets.GenericViewSet,
):
    serializer_class = serializers.ProjectSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = models.Project.objects.all()
    
    @decorators.parser_classes([MultiPartParser])
    def create(self, request):
        data = self.request.user.datasets.filter(id=self.request.data['data_id']).get()
        project = models.Project.objects.create(
            name=self.request.data['name'],
            related_user=self.request.user,
            related_data=data,
        )
        result_serializer = serializers.ProjectSerializer(project)
        return Response({
            "data": result_serializer.data,
            "status": status.HTTP_201_CREATED,
        })

    def retrieve(self, request, pk=None):
        queryset = self.request.user.projects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = serializers.ProjectSerializer(project)
        return Response({
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        })
    
    def list(self, request):
        result_queryset = self.queryset.filter(related_user=self.request.user)
        result_serializer = serializers.ProjectSerializer(result_queryset, many=True)
        return Response({
            "data": result_serializer.data,
            "status": status.HTTP_200_OK,
        })

class DatasetViewSet(
    mixins.CreateModelMixin, # .create(request) for creating a dataset for the user
    mixins.ListModelMixin, # .list(request) for listing all datasets of the user
    mixins.RetrieveModelMixin, # .retrieve(request) for returning a specify dataset
    viewsets.GenericViewSet,
):
    serializer_class = serializers.DatasetSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = models.Dataset.objects.all()
    
    @decorators.parser_classes([MultiPartParser])
    def create(self, request):
        dataset = models.Dataset.objects.create(
            name=self.request.data['name'],
            upload=self.request.data['upload'],
            related_user=self.request.user,
        )
        result_serializer = serializers.DatasetSerializer(dataset)
        return Response({
            "data": result_serializer.data,
            "status": status.HTTP_201_CREATED,
        })

    def retrieve(self, request, pk=None):
        import csv
        from io import StringIO
        queryset = self.request.user.datasets.all()
        dataset = get_object_or_404(queryset, pk=pk)
        serializer = serializers.DatasetSerializer(dataset)
        with open(dataset.upload.path, 'r') as f:
            header = next(csv.reader(StringIO(next(f)), delimiter=','))
        header = [{"index": idx, "label": label if label != '' else f'Unknown-{idx}'} for idx, label in enumerate(header)]
        return Response({
            "data": serializer.data,
            "header": header,
            "status": status.HTTP_200_OK,
        })
    
    def list(self, request):
        result_queryset = self.queryset.filter(related_user=self.request.user)
        result_serializer = serializers.DatasetSerializer(result_queryset, many=True)
        return Response({
            "data": result_serializer.data,
            "status": status.HTTP_200_OK,
        })

class JobViewSet(
    mixins.CreateModelMixin, # .create(request) for creating a job for the project
    mixins.ListModelMixin, # .list(request) for listing all jobs of the project
    mixins.RetrieveModelMixin, # .retrieve(request) for returning a specify job
    mixins.UpdateModelMixin, # .update(request) for updating
    viewsets.GenericViewSet,
):
    serializer_class = serializers.JobSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = models.Job.objects.all()

    @decorators.parser_classes([MultiPartParser])
    def create(self, request, project_pk=None,):
        project = self.request.user.projects.filter(id=project_pk).get()
        job = models.Job.objects.create(
            name=self.request.data['name'],
            related_project=project,
        )
        result_serializer = serializers.JobSerializer(job)
        return Response({
            "data": result_serializer.data,
            "status": status.HTTP_201_CREATED,
        })
    
    def retrieve(self, request, pk=None, project_pk=None):
        project = self.request.user.projects.filter(id=project_pk).get()
        queryset = project.jobs.all()
        job = get_object_or_404(queryset, pk=pk)
        serializer = serializers.JobSerializer(job)
        return Response({
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        })
    
    def list(self, request, project_pk=None):
        project = self.request.user.projects.filter(id=project_pk).get()
        result_queryset = self.queryset.filter(related_project=project)
        result_serializer = serializers.JobSerializer(result_queryset, many=True)
        return Response({
            "data": result_serializer.data,
            "status": status.HTTP_200_OK,
        })

    def partial_update(self, request, pk=None, project_pk=None):
        project = self.request.user.projects.filter(id=project_pk).get()
        queryset = project.jobs.all()
        job = get_object_or_404(queryset, pk=pk)
        serializer = serializers.JobSerializer(job)


@decorators.api_view(http_method_names=['GET'])
@decorators.authentication_classes([])
@decorators.permission_classes([])
def get_avaliable_models(request):
    
    """
    Return all avaliable model names
    """
    return Response({
        "data": model_hyper.get_models(),
        "status": status.HTTP_200_OK,
    })

@decorators.api_view(http_method_names=['GET'])
@decorators.authentication_classes([])
@decorators.permission_classes([])
def get_model_hp_description(request, model_name):
    from .ts_models import MODEL_HP_DESCRIPTIONS
    """
    Return hyperparams of specify model name
    """
    hp_description = model_hyper.get_model_hyper(model_name)
    if hp_description is not None:
        return Response({
            "data": hp_description,
            "status": status.HTTP_200_OK,
        })
    else:
        return Response({
            "data": hp_description,
            "status": status.HTTP_204_NO_CONTENT,
        })

