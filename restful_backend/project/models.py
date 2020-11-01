import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Dataset(models.Model):
    name = models.CharField(
        verbose_name='dataset name',
        help_text='the max length is 32, composed with "A-Za-z0-9_"',
        max_length=32,
        unique=False,
        null=False,
    )
    generated_uuid = str(uuid.uuid1())
    uuid = models.CharField(
        verbose_name='dataset uuid',
        help_text='generate uuid by uuid1 algorithm',
        max_length=36,
        default=generated_uuid,
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
        null=True,
    )