from django.db import models


class Job(models.Model):
    job_id = models.AutoField(
        verbose_name="system identifier of job",
        help_text="auto-increment in database",
        primary_key=True,
        blank=False,
        null=False,
    )
    job_name = models.CharField(
        verbose_name="job identifier for user",
        help_text="the max length is 32, composed with 'A-Za-z0-9_'",
        max_length=32,
        unique=False,
        null=False,
    )
    create_time = models.DateTimeField(
        verbose_name="the create time of job",
        help_text="the time at which the user created the job; auto-generated",
        unique=False,
        null=False,
    )
    modified_time = models.DateTimeField(
        verbose_name="the latest modified time of job",
        help_text="the time at which the configurations status changed",
        unique=False,
        null=False,
    )
    job_hash = models.BinaryField(
        verbose_name="the hash identifier of job",
        help_text="auto-generated hash based on time and random number",
        max_length=32,
        unique=False,
        null=False,
    )