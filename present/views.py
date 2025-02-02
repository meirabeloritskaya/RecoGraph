from rest_framework.viewsets import ModelViewSet
from django.views import View
from present.serializers import CategorySerializer, ProductSerializer
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render, get_object_or_404
from present.models import Category, Product, Favorite
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Exists, OuterRef


#  DRF API (Возвращает JSON)
class CategoryViewSet(ModelViewSet):
    """API для категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer]


class ProductViewSet(ModelViewSet):
    """API для товаров"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer]


#  Страницы (Отображает HTML)
class CategoryListView(View):
    """Выводит список всех категорий с картинками"""
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "present/all_product.html", {"categories": categories})


class CategoryDetailView(View):
    """Выводит список товаров в конкретной категории"""
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(category=category).annotate(
            is_favorite=Exists(
                Favorite.objects.filter(user=request.user, product=OuterRef('pk'))
            )
        )
        return render(request, "present/category_detail.html", {"category": category, "products": products})


class ToggleFavoriteView(View):
    """Добавление/удаление товара в избранное"""

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Требуется вход в систему"}, status=401)

        product = get_object_or_404(Product, id=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

        if not created:
            favorite.delete()
            return JsonResponse({"status": "removed"})

        return JsonResponse({"status": "added"})


class FavoritesListView(LoginRequiredMixin, ListView):
    """Выводит список избранных товаров"""
    model = Favorite
    template_name = "present/favorites.html"
    context_object_name = "favorites"

    def get_queryset(self):
        """Фильтруем избранные товары только для текущего пользователя"""
        return Favorite.objects.filter(user=self.request.user).select_related("product")