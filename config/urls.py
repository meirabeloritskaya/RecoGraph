from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/recipients/', include('recipients.urls')),
    path('api/events/', include('events.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/items/', include('items.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/analytics/', include('analytics.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)