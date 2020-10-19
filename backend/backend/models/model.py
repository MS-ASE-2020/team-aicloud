from django.db import models

class Model(models.model):
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
    
