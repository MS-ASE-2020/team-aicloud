from django.db import models
from . import User


class Data(models.Model):
    data_id = models.AutoField(
        verbose_name="system identifier of data",
        help_text="auto-increment in database",
        primary_key=True,
        blank=False,
        null=False,
    )
    data_name = models.CharField(
        verbose_name="data identifier for user",
        help_text="the max length is 32, composed with 'A-Za-z0-9_'",
        max_length=32,
        unique=False,
        null=False,
    )
    create_time = models.DateTimeField(
        verbose_name="the create time of data",
        help_text="the time at which the user uploaded the data; auto-generated",
        unique=False,
        null=False,
    )
    data_path = models.CharField(
        verbose_name="the store path of data in server",
        help_text="the max length is 256; auto-generated",
        max_length=256,
        unique=False,
        null=False,
    )
    data_hash = models.BinaryField(
        verbose_name="the hash identifier of data",
        help_text="auto-generated hash based on time and random number",
        max_length=32,
        unique=False,
        null=False,
    )
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