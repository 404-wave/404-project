from django.shortcuts import render

def home(request):
    # TODO: If the user is not authenticated then don't show the home page,
    # but instead show soe other page reporting the error. (Maybe just the login page).
    return render(request, 'home.html')


def profile(request):
    return render(request, 'profile.html')

