from django.db import models


class CmdStatus(models.IntegerChoices):
    UNCOMITTED = 0
    COMITTED = 1
    DONE = 2
    NOTIFIED = 3
    EXCEPTION = 4