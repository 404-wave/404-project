from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='user_index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('post_repos/', views.post_repos, name='post_repos'),
    path('list_events/', views.list_events, name='list_events'),
    path('event_details/<str:event_type>/', views.event_details, name='event_details')
]
