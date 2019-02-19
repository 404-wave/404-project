from django.urls import path

from . import views


# TODO:Make slug fields

urlpatterns = [
    path('', views.home, name='home'),
]
