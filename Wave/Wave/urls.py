from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from api.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'author', UserViewSet)

urlpatterns = [
    path('', include('users.urls')),
    path('home/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('service/', include(router.urls))
]
