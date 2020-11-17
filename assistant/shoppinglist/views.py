from django.http import HttpResponse


def index(request):
    """ This is a test """
    return HttpResponse("Hello")
