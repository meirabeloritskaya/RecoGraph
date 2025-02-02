from django.urls import path, include
from rest_framework.routers import DefaultRouter
from present.views import CategoryViewSet, ProductViewSet, CategoryListView, CategoryDetailView
from present.views import ToggleFavoriteView
from present.views import FavoritesListView

app_name = "present"

#  API маршруты
router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"products", ProductViewSet, basename="products")

#  HTML маршруты
urlpatterns = [
    path("api/", include(router.urls)),  # Подключаем API DRF
    path("categories/", CategoryListView.as_view(), name="all-products"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("favorites/<int:product_id>/toggle/", ToggleFavoriteView.as_view(), name="toggle-favorite"),
    path("favorites/", FavoritesListView.as_view(), name="favorites-list"),
]
