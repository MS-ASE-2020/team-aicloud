from django.db import models
from django.conf import settings
from django.utils import timezone


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


class Dataset(models.Model):
    name = models.CharField(
        verbose_name='dataset name',
        help_text='the max length is 32, composed with "A-Za-z0-9_"',
        max_length=32,
        unique=False,
        null=False,
    )
    time_created = models.DateTimeField(
        verbose_name='creation time',
        help_text='the time at which the user uploaded the data; auto-generated',
        null=False,
        default=timezone.now,
    )
    related_project = models.ForeignKey(
        Project,
        related_name='datasets',
        on_delete=models.CASCADE,
        help_text='dataset',
        null=False
    )
    upload = models.FileField(
        verbose_name='data file',
        upload_to='uploads',  # TODO: path <user>/<project>/
        null=False,
    )
