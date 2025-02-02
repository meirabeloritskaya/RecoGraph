from rest_framework.views import APIView
from recommendations.actions import (
    add_to_favorites,
    add_to_cart,
    mark_as_viewed,
    mark_as_bought,
)
from rest_framework.response import Response
from rest_framework import status
from recommendations.services import get_combined_recommendations
from django.shortcuts import render
from django.views import View
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class UserActionView(APIView):
    """
    API для выполнения действий пользователя (добавление в избранное, корзину, просмотр, покупка).
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get("product_id")
        action = kwargs.get("action")

        if not product_id:
            return Response(
                {"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if action == "favorite":
            return add_to_favorites(user, product_id)
        elif action == "cart":
            return add_to_cart(user, product_id)
        elif action == "view":
            return mark_as_viewed(user, product_id)
        elif action == "buy":
            return mark_as_bought(user, product_id)
        else:
            return Response(
                {"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
            )


class RecommendationsView(APIView):
    """
    API для получения объединенных рекомендаций через POST-запрос.
    """

    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt, name="dispatch")
    def post(self, request, *args, **kwargs):
        try:
            # Получаем параметры из тела запроса
            user_id = request.user.id
            gender = request.data.get("gender")
            age_range = request.data.get("age_range")
            # event_type = request.data.get("event_type")
            # relationship = request.data.get("relationship")
            top_n = request.data.get("top_n", 3)
            weights = request.data.get(
                "weights", {"knn": 3, "collaborative": 2, "pagerank": 1}
            )

            if not user_id:
                return Response(
                    {"error": "Параметр 'user_id' обязателен."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Генерация рекомендаций
            recommendations = get_combined_recommendations(
                user_id=user_id,
                gender=gender,
                age_range=age_range,
                # event_type=event_type,
                # relationship=relationship,
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
                {
                    "error": "Некорректные параметры. Проверьте значения 'user_id' и 'weights'."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RecommendationResultsView(View):
    def post(self, request):
        # Получение данных из формы
        gender = request.POST.get("gender")
        age_range = request.POST.get("age_range")

        # Проверка обязательных данных
        if not gender or not age_range:
            return render(
                request,
                "recommendations/results.html",
                {
                    "error": "Пол и возраст обязательны для заполнения.",
                },
            )

        #  Передаём параметры в get_combined_recommendations
        recommendations = get_combined_recommendations(
            user_id=request.user.id, gender=gender, age_range=age_range, top_n=5
        )

        # Рендеринг страницы с результатами
        return render(
            request,
            "recommendations/results.html",
            {
                "recommendations": recommendations,
                "gender": gender,
                "age_range": age_range,
            },
        )
