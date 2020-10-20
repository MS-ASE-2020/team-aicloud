from django.db import models

class ModelTypeChoice(models.IntegerChoices):
    INIT = 0
    PRETRAINED_RISHI = 1
    PRETRAINED_USER = 2
