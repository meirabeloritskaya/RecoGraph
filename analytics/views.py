from rest_framework.views import APIView
from rest_framework.response import Response
from recommendations.models import UserInteraction
from present.models import Product, Category
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db.models import Q


class TopProductsView(APIView):
    def get(self, request):
        """
        Возвращает топ-5 продуктов по популярности (количество взаимодействий).
        """
        top_products = (
            Product.objects.annotate(interaction_count=Count('interactions'))
            .order_by('-interaction_count')[:5]
        )
        data = [
            {"id": product.id, "name": product.name, "interaction_count": product.interaction_count}
            for product in top_products
        ]
        return Response(data)


class UserActionsStatsView(APIView):
    def get(self, request):
        """
        Возвращает распределение действий пользователей (просмотрено, куплено и т.д.).
        """
        actions_stats = (
            UserInteraction.objects.values('action')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        data = {stat['action']: stat['count'] for stat in actions_stats}
        return Response(data)


class SummaryAnalyticsView(APIView):
    def get(self, request):
        try:
            # Проверяем данные
            total_users = get_user_model().objects.count()
            total_products = Product.objects.count()

            # Проверка наличия взаимодействий
            total_interactions = UserInteraction.objects.aggregate(
                views=Count('id', filter=Q(action='view')),
                favorites=Count('id', filter=Q(action='favorite')),
                cart=Count('id', filter=Q(action='cart')),
                purchases=Count('id', filter=Q(action='buy')),
            )

            # Проверка категорий
            top_categories = Category.objects.annotate(
                interaction_count=Count('products__interactions')
            ).order_by('-interaction_count')[:3]

            # Проверка продуктов
            most_popular_products = Product.objects.annotate(
                interaction_count=Count('interactions')
            ).order_by('-interaction_count')[:3]

            # Формируем ответ
            data = {
                "total_users": total_users,
                "total_products": total_products,
                "total_interactions": total_interactions,
                "top_categories": [
                    {
                        "id": category.id,
                        "name": category.name,
                        "interaction_count": category.interaction_count,
                    }
                    for category in top_categories
                ],
                "most_popular_products": [
                    {
                        "id": product.id,
                        "name": product.name,
                        "interaction_count": product.interaction_count,
                    }
                    for product in most_popular_products
                ]
            }
            return Response(data, status=200)
        except Exception as e:
            # Возвращаем информацию об ошибке
            return Response({"error": str(e)}, status=500)