from django.http import JsonResponse

data = {
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
                'val': 50
            },
            {
                "time": '20200821',
                'val': 60
            },
    ]
}

def result(request, model_id):
    with open("test_result.csv", 'wb') as f:
        f.write(request.body)
    return JsonResponse(data)
    
