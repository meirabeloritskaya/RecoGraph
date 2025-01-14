from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipientsViewSet

router = DefaultRouter()
router.register(r'recipients', RecipientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
