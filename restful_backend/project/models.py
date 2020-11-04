import uuid
from django.db import models
from django.conf import settings
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


class Project(models.Model):
    name = models.CharField(
        verbose_name='project name',
        help_text='the max length is 32, composed with "A-Za-z0-9_"',
        max_length=32,
        null=False,
    )
    time_created = models.DateTimeField(
        verbose_name='creation time',
        help_text='the time at which the user created the project; auto-generated',
        null=False,
        default=timezone.now,
    )
    related_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='projects',
        on_delete=models.CASCADE,
        help_text='The user this project belongs to',
        null=False,
    )
    related_data = models.ForeignKey(
        Dataset,
        related_name='projects',
        on_delete=models.CASCADE,
        help_text='The data this project hold',
        null=False,
    )

class Job(models.Model):
    class JobStatus(models.IntegerChoices):
        UNCOMITTED = 0
        COMITTED = 1
        JOB_DONE = 2
        JOB_NOTIFIED = 3
    name = models.CharField(
        verbose_name="job identifier for user",
        help_text="the max length is 32, composed with 'A-Za-z0-9_'",
        max_length=32,
        unique=False,
        null=False,
    )
    hyper_params = PickledObjectField(
        null=True,
        blank=True,
    )
    user_config = PickledObjectField(
        null=True, 
        blank=True,
    )
    other_config = PickledObjectField(
        null=True, 
        blank=True,
    )
    status = models.IntegerField(
        choices=JobStatus.choices,
        default=JobStatus.UNCOMITTED,
    )
    time_created = models.DateTimeField(
        verbose_name='creation time',
        help_text='the time at which the user created the project; auto-generated',
        null=False,
        default=timezone.now,
    )
    related_project = models.ForeignKey(
        Project,
        related_name='jobs',
        on_delete=models.CASCADE,
        help_text='The project this job belongs',
        null=False,
    )

class Model(models.Model):
    name = models.CharField(
        verbose_name="name specified by user",
        help_text="the reasonable length is 8-32, composed with 'A-Za-z0-9_",
        max_length=32,
        default=crypto.get_random_string,
    )
    model_type = models.CharField(
        max_length=32,
        unique=False,
        null=False,
    )
    model_perf = PickledObjectField(
        verbose_name="model performace record",
        help_text="calculated via test. may be optional",
        null=True,
        blank=True,
    )
    model_file = models.FileField(
        upload_to='uploads/Models/', 
        null=True, 
        blank=True,
    )
    time_created = models.DateTimeField(
        verbose_name="the create time of model",
        help_text="the time when model created; auto-generated",
        null=True,
        blank=True,
    )