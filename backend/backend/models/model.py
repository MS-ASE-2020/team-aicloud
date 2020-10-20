from django.db import models
from . import User


class Model(models.Model):
    model_id = models.AutoField(
        verbose_name="identifier for model",
        help_text="auto-increment in database",
        primary_key=True)
    model_name = models.CharField(
        verbose_name="",
        help_text="the reasonable length is 8-32, composed with 'A-Za-z0-9_",
        max_length=32)
    model_perf = models.BinaryField(
        max_length=16,
        null=True,
        blank=True)
    save_path = models.CharField(
        max_length=256,
        null=True,
        blank=True)
    create_time = models.DateTimeField()
    model_hash = models.BinaryField(max_length=5)
    user_id = models.ForeignKey(
        User,
        to_field='user_id',
        on_delete=models.CASCADE,
        help_text="reference to TE_USER.USER_ID",
        blank=False,
        null=False,
    )
    user_access_id = models.ManyToManyField(
        User,
        related_name='to_access_users',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )