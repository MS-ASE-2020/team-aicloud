from django.conf import settings
from django.core.validators import int_list_validator
from django.db import models
from django.utils import timezone
from .status import CmdStatus
from .dataset import Dataset


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