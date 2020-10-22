from django.http import HttpResponse


def upload_data(request):
    with open("test.csv", 'wb') as f:
        f.write(request.body)
    return HttpResponse(status=200)