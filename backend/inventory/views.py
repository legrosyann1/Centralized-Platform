from django.http import HttpResponse


def inventory(request):
    return HttpResponse("Hello, world. You're at the inventory.")