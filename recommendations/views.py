
from rest_framework.views import APIView
from recommendations.actions import add_to_favorites, add_to_cart, mark_as_viewed, mark_as_bought
from rest_framework.response import Response
from rest_framework import status
from recommendations.services import get_combined_recommendations


class UserActionView(APIView):
    """
    API для выполнения действий пользователя (добавление в избранное, корзину, просмотр, покупка).
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')
        action = kwargs.get('action')

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'favorite':
            return add_to_favorites(user, product_id)
        elif action == 'cart':
            return add_to_cart(user, product_id)
        elif action == 'view':
            return mark_as_viewed(user, product_id)
        elif action == 'buy':
            return mark_as_bought(user, product_id)
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)


class RecommendationsView(APIView):
    """
    API для получения объединенных рекомендаций через POST-запрос.
    """

    def post(self, request, *args, **kwargs):
        try:
            # Получаем параметры из тела запроса
            user_id = request.data.get("user_id")
            top_n = request.data.get("top_n", 3)
            weights = request.data.get("weights", {
                "knn": 3,
                "collaborative": 2,
                "pagerank": 1
            })

            if not user_id:
                return Response(
                    {"error": "Параметр 'user_id' обязателен."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Генерация рекомендаций
            recommendations = get_combined_recommendations(
                user_id=int(user_id),
                top_n=int(top_n),
                weights=weights,
            )

            # Формируем JSON-ответ
            response_data = [
                {"id": product.id, "name": product.name} for product in recommendations
            ]

            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError:
            return Response(
                {"error": "Некорректные параметры. Проверьте значения 'user_id' и 'weights'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )