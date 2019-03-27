from django.urls import path, include

from . import views
import friends.views


urlpatterns = [
    path('', views.home, name='home'),
    path('friends/', include('friends.urls')),
    path('friends/', views.friends, name='my_friends'),
    path('profile/', views.profile, name='my_profile'),
    path('profile/<uuid:pk>', views.profile, name='profile'),
    path('profile/edit/',views.edit_profile,name='edit_profile'),
    path('profile/<str:value>', views.profile, name='profile'), 
    path('profile/follow/', friends.views.follow, name='follow'),
    path('profile/unfollow/', friends.views.unfollow, name='unfollow'),
]
