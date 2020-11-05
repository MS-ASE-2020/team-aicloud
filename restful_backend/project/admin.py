from django.contrib import admin
from .models import Dataset, Job, Predictor

# Register your models here.
admin.site.register(Dataset)
admin.site.register(Job)
admin.site.register(Predictor)