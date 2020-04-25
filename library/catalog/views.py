from django.shortcuts import HttpResponse, render


def catalog_home(request):
    return HttpResponse("Hello Catalog!")
