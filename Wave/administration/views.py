from django.shortcuts import render

from django.http import HttpResponseForbidden

def administration(request):

    if request.user.is_authenticated:
        if request.user.is_admin:
            return render(request, 'administration.html')
    else:
        return HttpResponseForbidden()
