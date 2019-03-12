from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from rest_framework import routers

from api.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'author', UserViewSet)

#Note that the default login_url for django is '/accounts/login' which will 404
@login_required(login_url='/login/')
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)

urlpatterns = [
    path('', include('users.urls')),
    path('home/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('service/', include(router.urls)),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
