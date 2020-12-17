from django.db import models
from django.utils import timezone, crypto
from picklefield.fields import PickledObjectField
from .series import Series
from .status import CmdStatus
from ..utils.dataset_utils import model_file_path

class Predictor(models.Model):
    name = models.CharField(
        verbose_name="name specified by user",
        help_text="the reasonable length is 8-32, composed with 'A-Za-z0-9_",
        max_length=32,
        default=crypto.get_random_string,
    )
    model_file = PickledObjectField(
        editable=True
    )
    status = models.IntegerField(
        choices=CmdStatus.choices,
        default=CmdStatus.CREATED,
    )
    model_save = models.FileField(
        verbose_name='data file',
        upload_to=model_file_path,  # TODO: path <user>/<project>/
        null=True,
        blank=True
    )
    time_created = models.DateTimeField(
        verbose_name="the create time of model",
        help_text="the time when model created; auto-generated",
        null=True,
        blank=False,
        default=timezone.now,
    )
    related_series = models.ForeignKey(
        Series,
        related_name="predictor",
        null=False,
        blank=False,
        default=0,
        on_delete=models.CASCADE
    )