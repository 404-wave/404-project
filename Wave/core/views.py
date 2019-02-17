from django.shortcuts import render


# TODO: use the REST API once it is established
def home(request):

    return render(request, 'home.html')
