from django.http import JsonResponse

def user_login(request):
    data = {
        'code': 20000
    }
    return JsonResponse(data)