from django.db import models
from django.db.models import IntegerChoices

class Configuration(models.Model):
    class ConfigStatus(IntegerChoices):
        UNCOMITTED = 0
        COMITTED = 1
        JOB_DONE = 2
        JOB_NOTIFIED = 3
        
    config_id = models.AutoField(primary_key=True)
    config_name = models.CharField(max_length=32)
    model_type = models.IntegerField()
    hyper_params = models.FileField(upload_to='uploads/Config/HyperParams')
    user_config = models.FileField(upload_to='uploads/Config/UserConfig', null=True, blank=True)
    other_config = models.FileField(upload_to='uploads/Config/OtherConfig', null=True, blank=True)
    create_time = models.TimeField()
    config_hash = models.BinaryField(max_length=32)
    config_status = models.IntegerField(choices=ConfigStatus)
    
        
        