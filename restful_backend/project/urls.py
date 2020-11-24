from django.urls import path, re_path, include
from . import views
from rest_framework_nested import routers
import private_storage.urls

app_name = 'project'

router = routers.SimpleRouter()
router.register('job', views.JobViewSet)
router.register('data', views.DatasetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('model/', views.get_avaliable_models),
    path('model/<str:model_name>', views.get_model_hp_description),
    path("files/", views.DatasetViewSet.as_view({"get": "retrieve"}), name="serve_private_file"),
    path('files/', include(private_storage.urls)),
]
