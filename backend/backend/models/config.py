from django.db import models
from django.db.models import IntegerChoices
from .job import Job

class Config(models.Model):
    class ConfigStatus(IntegerChoices):
        UNCOMITTED = 0
        COMITTED = 1
        JOB_DONE = 2
        JOB_NOTIFIED = 3
        
    config_id = models.AutoField(
        verbose_name="identifier for configuration",
        help_text="auto-increment in database",
        primary_key=True)
    job_id = models.ForeignKey(
        Job,
        to_field="job_id",
        help_text="reference TE_JOB_JOB_ID"
    )
    config_name = models.CharField(
        verbose_name="name for user to identifier",
        help_text="the max length is 32, composed with 'A-Za-z0-9_'", 
        max_length=32)
    hyper_params = models.FileField(
        upload_to='uploads/Config/HyperParams')
    user_config = models.FileField(
        upload_to='uploads/Config/UserConfig', 
        null=True, 
        blank=True)
    other_config = models.FileField(
        upload_to='uploads/Config/OtherConfig', 
        null=True, 
        blank=True)
    create_time = models.DateTimeField()
    config_hash = models.BinaryField(
        max_length=32)
    config_status = models.IntegerField(
        choices=ConfigStatus)
    
        
        