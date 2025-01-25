
from rest_framework.views import APIView
from recommendations.actions import add_to_favorites, add_to_cart, mark_as_viewed, mark_as_bought
from recommendations.engine import RecommendationEngine
from rest_framework.response import Response
from present.models import Product
from rest_framework import status


class AddToFavoriteView(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        return add_to_favorites(user, product_id)


class AddToCartView(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        return add_to_cart(user, product_id)


class MarkAsViewedView(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        return mark_as_viewed(user, product_id)


class MarkAsBoughtView(APIView):
    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        return mark_as_bought(user, product_id)


class RecommendationView(APIView):
    def post(self, request):
        """
        Принимает параметры получателя и возвращает рекомендации.
        """
        user_id = request.user.id
        recipient_data = request.data

        # Проверка на наличие необходимых параметров
        required_fields = ['gender', 'age_range', 'event_type', 'relationship', 'price']
        for field in required_fields:
            if field not in recipient_data:
                return Response(
                    {"error": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Получаем рекомендации
        engine = RecommendationEngine(user_id)
        recommendations = engine.get_recommendations(
            gender=recipient_data['gender'],
            age_range=recipient_data['age_range'],
            event_type=recipient_data['event_type'],
            relationship=recipient_data['relationship'],
            price=recipient_data['price'],
            top_n=3  # Количество рекомендаций
        )

        return Response({
            "recommendations": recommendations
        }, status=status.HTTP_200_OK)

