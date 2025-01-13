from django.contrib import admin
from django.urls import path, include

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
