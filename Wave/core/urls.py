from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('friends/', include('friends.urls')),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>', views.profile, name='profile'), # TODO: Change to <uuid:pk> when implemented
]
