from django.db import models


class CmdStatus(models.IntegerChoices):
    CREATED = 0
    UNCOMITTED = 1
    COMITTED = 2
    DONE = 3
    EXCEPTION = 4