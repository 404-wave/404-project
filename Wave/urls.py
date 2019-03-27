from django.contrib.auth.decorators import login_required
from django.contrib import admin

from django.conf.urls.static import static
from django.conf.urls import include, url

from django.urls import include, path
from django.conf import settings

from django.views.static import serve


#https://blog.majsky.cz/django-protected-media-files/
#Credit: Michal Májský
#Note that the default login_url for django is '/accounts/login' which will 404
# @login_required(login_url='/login/')
# def protected_serve(request, path, document_root=None, show_indexes=False):
#     return serve(request, path, document_root, show_indexes)

base64_pattern = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'

urlpatterns = [
    path('posts/', include('posts.urls')),
    path('home/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),

    path('api-auth/', include('rest_framework.urls')),
    path('service/', include('api.urls')),
    path('api/', include('api.urls')), # TODO: Verify
    path('', include('api.urls')), # TODO: Verify no conflict
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
