from django.db import models


class User(models.Model):
    user_id = models.AutoField(
        verbose_name="system identifier of user",
        help_text="auto-increment in database",
        primary_key=True,
        blank=False,
        null=False,
    )
    user_name = models.CharField(
        verbose_name="client identifier of user",
        help_text="the reasonable length is 4-16, composed with 'A-Za-z0-9_'",
        max_length=16,
        unique=True,
        null=False,
    )
    email = models.CharField(
        verbose_name="the email of user",
        help_text="should be compliance with email address spec",
        max_length=32,
        unique=True,
        null=False,
    )
    password = models.BinaryField(
        verbose_name="the encrypted user password",
        help_text="the reasonable length is 8-16, composed with 'A-Za-z0-9_',"\
            " stored after SHA-256 encrypt",
        max_length=32,
        unique=False,
        null=False,
    )