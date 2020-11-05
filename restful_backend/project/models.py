import uuid
from django.conf import settings
from django.core.validators import int_list_validator
from django.db import models
from django.utils import timezone, crypto
from picklefield.fields import PickledObjectField


class Dataset(models.Model):
    name = models.CharField(
        verbose_name='dataset name',
        help_text='the max length is 32, composed with "A-Za-z0-9_"',
        max_length=32,
        unique=False,
        null=False,
    )
    uuid = models.UUIDField(
        verbose_name='dataset uuid',
        help_text='generate uuid by uuid1 algorithm',
        default=uuid.uuid4,
        editable=False,
    )
    time_created = models.DateTimeField(
        verbose_name='creation time',
        help_text='the time at which the user uploaded the data; auto-generated',
        null=False,
        default=timezone.now,
    )
    upload = models.FileField(
        verbose_name='data file',
        upload_to='uploads',  # TODO: path <user>/<project>/
        null=False,
    )
    related_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='datasets',
        on_delete=models.CASCADE,
        help_text='The user this dataset belongs to',
        null=False,
    )

class CmdStatus(models.IntegerChoices):
    UNCOMITTED = 0
    COMITTED = 1
    DONE = 2
    NOTIFIED = 3
    EXCEPTION = 4

class Job(models.Model):
    name = models.CharField(
        verbose_name="job identifier for user",
        help_text="the max length is 32, composed with 'A-Za-z0-9_'",
        max_length=32,
        unique=False,
        null=False,
    )
    status = models.IntegerField(
        choices=CmdStatus.choices,
        default=CmdStatus.UNCOMITTED,
    )
    time_created = models.DateTimeField(
        verbose_name='creation time',
        help_text='the time at which the user created the project; auto-generated',
        null=False,
        default=timezone.now,
    )
    groupby_indexs = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        default=None,
        validators=[int_list_validator],
    )
    target_indexs = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        default=None,
        validators=[int_list_validator],
    )
    timestamp_indexs = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        default=None,
        validators=[int_list_validator],
    )
    related_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='jobs',
        on_delete=models.CASCADE,
        help_text='The user this job belongs to',
        null=False,
    )
    related_data = models.ForeignKey(
        Dataset,
        related_name='jobs',
        on_delete=models.CASCADE,
        help_text='The data this job hold',
        null=False,
    )

class Series(models.Model):
    cluster_key = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        default=None,
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

class Predictor(models.Model):
    name = models.CharField(
        verbose_name="name specified by user",
        help_text="the reasonable length is 8-32, composed with 'A-Za-z0-9_",
        max_length=32,
        default=crypto.get_random_string,
    )
    model_file = PickledObjectField()
    status = models.IntegerField(
        choices=CmdStatus.choices,
        default=CmdStatus.UNCOMITTED,
    )
    time_created = models.DateTimeField(
        verbose_name="the create time of model",
        help_text="the time when model created; auto-generated",
        null=True,
        blank=False,
        default=None,
    )