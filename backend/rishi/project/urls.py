from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.ProjectListCreateView.as_view(), name='list_create'),
]