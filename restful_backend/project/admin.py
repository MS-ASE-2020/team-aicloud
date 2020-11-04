from django.contrib import admin
from .models import Dataset, Project, Job, Model

# Register your models here.
admin.site.register(Dataset)
admin.site.register(Project)
admin.site.register(Job)
admin.site.register(Model)