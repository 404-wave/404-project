from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# def posts_index(request):
#     return HttpResponse("<h1> Hello. You're at the posts index. </h1>")


def posts_create(request):
    return HttpResponse("<h1> Create a posts. </h1>")


def posts_detail(request):
    return HttpResponse("<h1> Detail a posts. </h1>")


def posts_list(request):
    return HttpResponse("<h1> List a posts. </h1>")


def posts_update(request):
    return HttpResponse("<h1> Update a posts. </h1>")


def posts_delete(request):
    return HttpResponse("<h1> Delete a posts. </h1>")
