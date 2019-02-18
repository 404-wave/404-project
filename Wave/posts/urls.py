from django.conf.urls import url
from . import views

urlpatterns = [
    # url('', views.posts_index, name='posts'),
    # url('', views.posts_list, name="posts"),
    # url('create/', views.posts_create, name="create"),
    # url('detail/', views.posts_detail, name="detail"),
    # url('update/', views.posts_update, name="update"),
    # url('delete/', views.posts_delete, name="delete"),

    url(r'^$', views.posts_list),
    url(r'^create/$', views.posts_create),
    url(r'detail/(?P<id>\d+)/$', views.posts_detail, name='detail'),
    url(r'update/$', views.posts_update),
    url(r'delete/$', views.posts_delete),
]
