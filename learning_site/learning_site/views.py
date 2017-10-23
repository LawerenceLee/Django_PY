from django.http import HttpResponse


def hello_world(requeset):
    return HttpResponse('Hello World')