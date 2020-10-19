from django.db import models


class Project(models.Model):
    project_id = models.AutoField(
        verbose_name="system identifier of project",
        help_text="auto-increment in database",
        primary_key=True,
        blank=False,
        null=False,
    )
    project_name = models.CharField(
        verbose_name="project identifier for user",
        help_text="the max length is 32, composed with 'A-Za-z0-9_'",
        max_length=32,
        unique=False,
        null=False,
    )
    create_time = models.DateTimeField(
        verbose_name="the create time of project",
        help_text="the time at which the user created the project; auto-generated",
        unique=False,
        null=False,
    )
    project_hash = models.BinaryField(
        verbose_name="the hash identifier of project",
        help_text="auto-generated hash based on time and random number",
        max_length=32,
        unique=False,
        null=False,
    )