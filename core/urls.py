from django.urls import path, include

from . import views
import friends.views


# TODO:Make slug fields

urlpatterns = [
    path('', views.home, name='home'),
    path('friends/', views.friends, name='my_friends'),
    path('friends/', include('friends.urls')),
    path('profile/', views.profile, name='my_profile'),
    path('profile/<uuid:pk>', views.profile, name='profile'), # TODO: Change to <uuid:pk> when implemented
    path('profile/<str:value>', views.profile, name='profile'), # TODO: Change to <uuid:pk> when implemented
    path('profile/follow/', friends.views.follow, name='follow'),
    path('profile/unfollow/', friends.views.unfollow, name='unfollow'),
    path('profile/edit/',views.edit_profile,name='edit_profile')
]
