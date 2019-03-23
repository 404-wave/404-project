from django.conf.urls import url
from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth.decorators import login_required
from django.views.static import serve


# TODO:Make slug fields

#https://blog.majsky.cz/django-protected-media-files/
#Credit: Michal Májský
#Note that the default login_url for django is '/accounts/login' which will 404
# @login_required(login_url='/login/')
# def protected_serve(request, path, document_root=None, show_indexes=False):
#     return serve(request, path, document_root, show_indexes)

urlpatterns = [
    # url('', views.posts_index, name='posts'),
    # url('', views.posts_list, name="posts"),
    # url('create/', views.posts_create, name="create"),
    # url('detail/', views.posts_detail, name="detail"),
    # url('update/', views.posts_update, name="update"),
    # url('delete/', views.posts_delete, name="delete"),

    # url(r'^$', views.posts_list, name='list'),
    # url(r'^create/$', views.posts_create),


    #url(r'detail/(?P<id>\d+)/$', views.posts_detail, name='posts-detail'),
    path('detail/<uuid:id>/', views.posts_detail, name='posts-detail'),
    #url(r'(?P<id>\d+)/edit/$', views.posts_update, name='posts-update'),
    path('<uuid:id>/edit/', views.posts_update, name='posts-update'),
    #url(r'(?P<id>\d+)/delete/$', views.posts_delete, name='posts-delete'),
    path('<uuid:id>/delete/', views.posts_update, name='posts-delete'),
    #url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
]
