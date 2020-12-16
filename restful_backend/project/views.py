from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication, permissions, decorators, viewsets, mixins, status
from rest_framework.decorators import APIView, action
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from . import models
from . import serializers
from .utils import *
import json
from . import trainer

# Create your views here.
class JobViewSet(
    mixins.CreateModelMixin, # .create(request) for creating a project for the user
    mixins.ListModelMixin, # .list(request) for listing all projects of the user
    mixins.RetrieveModelMixin, # .retrieve(request) for returning a specify project
    mixins.UpdateModelMixin, # .update(request) for updating
    viewsets.GenericViewSet,
    mixins.DestroyModelMixin,
):
    serializer_class = serializers.JobSerializer
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = models.Job.objects.all()
    
    @decorators.parser_classes([MultiPartParser])
    def create(self, request):
        data = self.request.user.datasets.filter(id=self.request.data['data_id']).get()
        job = models.Job.objects.create(
            name=self.request.data['name'],
            related_user=self.request.user,
            related_data=data,
        )
        result_serializer = serializers.JobSerializer(job)
        return Response({
            "data": result_serializer.data,
            "status": status.HTTP_201_CREATED,
        })

    def retrieve(self, request, pk=None):
        queryset = self.request.user.jobs.all()
        job = get_object_or_404(queryset, pk=pk)
        serializer = serializers.JobSerializer(job)
        return Response({
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        })
    
    def list(self, request):
        result_queryset = self.queryset.filter(related_user=self.request.user)
        result_serializer = serializers.JobSerializer(result_queryset, many=True)
        return Response({
            "data": result_serializer.data,
            "status": status.HTTP_200_OK,
        })

    """
    add indices configuration: traget, time_stamp, group_by
    and create series
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        group_by_indices = self.request.data["groupby_indexs"]
        dataset_path = self.get_object().related_data.upload
        group_by_vals = dataset_utils.slice_dataset(dataset_path, group_by_indices)
        # create series 
        for val in group_by_vals:
            ts = models.Series.objects.create(
                cluster_key=val,
                related_job=self.get_object(),
                related_data=self.get_object().related_data
            )

        return super().update(request, *args, **kwargs)

    """
    add configuration for related_ts: features, models, model_hyper-paramter
    change series status to uncomitted
    start model_training
    """
    def partial_update(self, request, pk):
        series = self.request.data
        queryset = self.request.user.jobs.all()
        results = list()
        for ts in series:
            ts_obj = models.Series.objects.get(pk=ts['ts_id'])
            if 'auto_tune_metric' not in ts:
                ts['auto_tune_metric'] = ''
            predictor = models.Predictor.objects.create(
                name=ts['model_name'],
                status=models.CmdStatus.COMITTED,
                model_file={
                    'hyper_params': ts['hyper_params'],
                    'eval_metrics': ts['eval_metrics'],
                    'auto_tune_metric': ts['auto_tune_metric'],
                    'auto_tune': ts['auto_tune'],
                    'max_eval': ts['max_eval']
                },
                related_series=ts_obj
            )
            ts_serializer = serializers.SeriesSerializer(
                ts_obj,
                data={
                    'feature_indexs': ts["feature_indexs"]
                },
                partial=True
            )
            ts_serializer.is_valid(raise_exception=True)
            ts_result = ts_serializer.save()
            dataset = dataset_utils.get_sliced_dataset(self.get_object().related_data.upload, self.get_object().groupby_indexs, ts_obj.cluster_key)
            # sm.commit_job(ts_serializer.data)
            job_obj = self.get_object()
            _, target_idx, ts_idx = dataset_utils.str2list(job_obj)
            feature_idx = dataset_utils.str2listofint(ts["feature_indexs"])
            model = trainer.trainer(
                model_name=ts['model_name'], 
                config=ts['hyper_params'], 
                metrics=ts["eval_metrics"],
                auto_tune_metric=ts['auto_tune_metric'],
                auto_tune=ts["auto_tune"],
                max_eval=ts["max_eval"])
            metrics, config, tuned_model = model.train(dataset, target_idx, ts_idx, feature_idx)
            predictions, timestamps = model.predict(ts["next_k_prediction"])
            # save into predictors
            model_file = {
                'predictions': predictions,
                'timestamps': timestamps,
                'metrics': metrics,
                'config': config,
                # 'model': tuned_model
            }
            p_serializer = serializers.PredictorSerializer(
                predictor,
                data={
                    'model_file': model_file,
                    'status': models.CmdStatus.DONE,
                },
                partial=True
            )
            p_serializer.is_valid(raise_exception=True)
            p_serializer.save()
            model_file["ts_id"] = ts["ts_id"]
            model_file["model_name"] = ts['model_name']
            results.append(model_file)        

        job_obj = get_object_or_404(queryset, pk=pk)
        job_serializer = self.get_serializer(
            job_obj,
            data={'status': models.CmdStatus.DONE},
            partial=True
        )
        job_serializer.is_valid(raise_exception=True)
        job_result = job_serializer.save()
        
        return Response(
            status=status.HTTP_200_OK,
            data=results
        )

    @action(methods=['patch'], detail=True, url_path='update_all', url_name='update_all')
    def partial_update_all(self, request, pk=None):
        series = self.get_object().series.all()
        tss = request.data
        for ts in tss:
            if 'auto_tune_metric' not in ts:
                ts['auto_tune_metric'] = ''
            for ts_obj in series:
                predictor = models.Predictor.objects.create(
                    name=ts['model_name'],
                    status=models.CmdStatus.COMITTED,
                    model_file={
                        'hyper_params': ts['hyper_params'],
                        'eval_metrics': ts['eval_metrics'],
                        'auto_tune_metric': ts['auto_tune_metric'],
                        'auto_tune': ts['auto_tune'],
                        'max_eval': ts['max_eval']
                    },
                    related_series=ts_obj
                )
                ts_serializer = serializers.SeriesSerializer(
                    ts_obj,
                    data={
                        'feature_indexs': ts["feature_indexs"]
                    },
                    partial=True
                )
                ts_serializer.is_valid(raise_exception=True)
                ts_result = ts_serializer.save()
                # TODO: commit job to scheduler
        
        return Response(
            status=status.HTTP_200_OK
        )

    """
    return series' available features, groupby_key, groupby_val
    """
    @action(methods=['get'], detail=True, url_path='ts_details', url_name='ts_details')
    def get_ts_details(self, request, pk=None):
        import pandas as pd
        job_obj = self.get_object()
        # FIXME: csv reading may be redundant
        data_path = job_obj.related_data.upload.path
        df = pd.read_csv(data_path)
        headers = df.columns
        groupby_key, target_idx, ts_idx = dataset_utils.str2list(job_obj)
        groupby_key = list(map(lambda x: headers[int(x)], groupby_key))
        features = list(set(headers) - set(groupby_key) - set([headers[target_idx]]) - set([headers[ts_idx]]))
        ts_details = [{"ts_id": x.pk, "groupby_val": x.cluster_key} for x in job_obj.series.all()]
        return Response(
            status=status.HTTP_200_OK,
            data={
                "features": features,
                "groupby_key": groupby_key,
                "ts_details": ts_details
            }
        )

    @action(methods=['get'], detail=True, url_path='job_results', url_name='job_results')
    def get_job_results(self, request, pk=None):
        job_obj = self.get_object()
        groupby_key, target_idx, ts_idx = dataset_utils.str2list(job_obj)
        if job_obj.status != models.CmdStatus.DONE:
            return Response(
                status=status.HTTP_200_ok,
                data={
                    'stauts': job_obj.status
                }
            )

        series = job_obj.series.all()
        results = []
        for ts in series:
            ts_results = []
            ts_history = dataset_utils.get_sliced_dataset(
                job_obj.related_data.upload.path, job_obj.groupby_indexs, ts.cluster_key)
            ts_history = ts_history.iloc[:, [target_idx, ts_idx]]
            for predictor in ts.predictor.all():
                if predictor.status == models.CmdStatus.DONE:
                    model_file = predictor.model_file
                    model_file["ts_id"] = ts.id
                    model_file["model_name"] = predictor.name
                    model_file["ts_history"] = ts_history
                    ts_results.append(model_file)
            
            results.append({
                'ts_id': ts.id,
                'results': ts_results
            })

        return Response(
            status=status.HTTP_200_OK,
            data={
                'status': self.get_object().status,
                'results': results
            }
        )

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class DatasetViewSet(
    mixins.CreateModelMixin, # .create(request) for creating a dataset for the user
    mixins.ListModelMixin, # .list(request) for listing all datasets of the user
    mixins.RetrieveModelMixin,  # .retrieve(request) for returning a specify dataset
    mixins.DestroyModelMixin,
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
        heads = dataset_utils.preview(dataset.upload)
        return Response({
            "data": serializer.data,
            "header": header,
            "status": status.HTTP_200_OK,
            "heads": heads,
            "time_created": dataset.time_created
        })
    
    def list(self, request):
        dataset = [{"name": x.name, "id": x.pk, "time_created": x.time_created} for x in self.request.user.datasets.all()]

        return Response(
            status=status.HTTP_200_OK,
            data=dataset
        )

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

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

