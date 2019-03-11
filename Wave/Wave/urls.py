from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('users.urls')),
    path('home/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('service/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
