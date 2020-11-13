from django.core.validators import int_list_validator
from django.db import models
from .job import Job
from .dataset import Dataset

class Series(models.Model):
    cluster_key = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        default=None,
    )
    status = models.IntegerField(
        choices=CmdStatus.choices,
        default=CmdStatus.CREATED,
    )
    feature_indexs = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        default=None,
        validators=[int_list_validator],
    )
    related_job = models.ForeignKey(
        Job,
        related_name='series',
        on_delete=models.CASCADE,
        help_text='The job that contains the series',
        null=False,
    )
    related_data = models.ForeignKey(
        Dataset,
        related_name='series',
        on_delete=models.CASCADE,
        help_text='The data this series connect',
        null=False,
    )