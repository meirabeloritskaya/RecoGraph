from django.urls import path, include
from rest_framework.routers import DefaultRouter
from present.views import (
    CategoryViewSet,
    ProductViewSet,
    CategoryListView,
    CategoryDetailView,
)
from present.views import ToggleFavoriteView
from present.views import FavoritesListView, AddToCartView, RemoveFromCartView, CartView
from present.views import ProductDetailView


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
    path(
        "favorites/<int:product_id>/toggle/",
        ToggleFavoriteView.as_view(),
        name="toggle-favorite",
    ),
    path("favorites/", FavoritesListView.as_view(), name="favorites-list"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/<int:product_id>/", AddToCartView.as_view(), name="add-to-cart"),
    path(
        "cart/remove/<int:product_id>/",
        RemoveFromCartView.as_view(),
        name="remove-from-cart",
    ),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    # path("api/cart/", CartListView.as_view(), name="cart-list"),  # API для Postman
]
