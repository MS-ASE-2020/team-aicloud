import os
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes, api_view
from rest_framework.parsers import MultiPartParser
from django.conf import settings


def upload_data(request):
    OUTPUT_PATH = "D:/Uploaded"
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    uploaded_file = request.FILES['file']
    # uploaded_filename = uploaded_file.name
    file_uuid = str(uuid.uuid1())
    with open(os.path.join(OUTPUT_PATH, file_uuid + '.csv'), 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
    return JsonResponse({"code": 20000, "uuid": file_uuid})


class DatasetView(APIView):
    FILE_PATH = settings.FILE_UPLOAD_PATH
    os.makedirs(FILE_PATH, exist_ok=True)

    @parser_classes([MultiPartParser])
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        example_data = {
            'code': 20000,
            'data':
                {
                    'model_name': 'linearfit',
                    'hyperparameter': {
                        'lastest_len': 5,
                        'hyperparameter': "string"
                    },
                    'metric': [
                        {
                            'name': 'acc',
                            'val': 1.0
                        }
                    ],
                    'predicted':
                    [
                        {
                            'time': '20200821',
                            'val': 70
                        },
                        {
                            "time": '20200821',
                            'val': 60
                        },
                    ]
                }
        }
        return JsonResponse(example_data)

    @parser_classes([MultiPartParser])
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        # uploaded_filename = uploaded_file.name
        file_uuid = str(uuid.uuid1())
        with open(os.path.join(self.FILE_PATH, file_uuid + '.csv'), 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        return JsonResponse({"code": 20000, "uuid": file_uuid})
