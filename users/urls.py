from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='user_index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register')
]
