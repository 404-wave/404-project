from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="user_index"),
    path('register/', views.register, name="register")
]
