from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
    path('', views.DatasetView.as_view()),
]