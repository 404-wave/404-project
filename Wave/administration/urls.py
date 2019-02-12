from django.urls import path

from . import views

urlpatterns = [
    path('', views.administration, name='administration'),
]
