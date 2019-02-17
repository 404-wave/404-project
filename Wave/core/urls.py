from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>', views.profile, name='profile'), # TODO: Change to <uuid:pk> when implemented
]
