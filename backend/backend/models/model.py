from django.db import models
from . import User
from . import Config
from . import ModelTypeChoice

class Model(models.Model):
    model_id = models.AutoField(
        verbose_name="identifier for model",
        help_text="auto-increment in database",
        primary_key=True)
    config_id = models.ForeignKey(
        Config, 
        to_field="config_id",
        on_delete=models.CASCADE,
        help_text="reference to TE_CONFIG_CONFIGID")
    model_name = models.CharField(
        verbose_name="name specified by user",
        help_text="the reasonable length is 8-32, composed with 'A-Za-z0-9_",
        max_length=32)
    model_type = models.Choices(
        ModelTypeChoice,
        help_text="model type description such as pretrained etc."
    )
    model_perf = models.BinaryField(
        verbose_name="model performace record",
        help_text="calculated via test. may be optional",
        max_length=16,
        null=True,
        blank=True)
    save_path = models.CharField(
        verbose_name="trained models save path",
        help_text="trained models save path, should be in save_models/**",
        max_length=256,
        null=True,
        blank=True)
    create_time = models.DateTimeField(
        verbose_name="the create time of model",
        help_text="the time when model created; auto-generated")
    model_hash = models.BinaryField(
        verbose_name="the hash identifier of model",
        help_text="auto-generated hash based on time and random number",
        max_length=5)