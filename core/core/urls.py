from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from common.swagger import schema_view

BASE_NAME = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{BASE_NAME}/v1.0/', include('api.v1.urls')),
    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    developerment_urls = [
        path('swagger/api.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

    developerment_urls += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    developerment_urls += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += developerment_urls
