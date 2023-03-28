from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from animesearch import settings
from .yasg import urlpatterns as doc_urls

api_version = 'v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('anime.urls')),
    path('api/', include('user.urls')),
    path('api/auth/', include('djoser.urls')),
    re_path('api/auth/', include('djoser.urls.authtoken')),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
