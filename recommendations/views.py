
from rest_framework.views import APIView
from recommendations.actions import add_to_favorites, add_to_cart, mark_as_viewed, mark_as_bought
from recommendations.engine import RecommendationEngine
from rest_framework.response import Response
from rest_framework import status
from recommendations.graph import build_graph


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
        Принимает параметры получателя и возвращает рекомендации (метод POST).
        """
        user_id = request.user.id
        recipient_data = request.data

        # Проверка на наличие необходимых параметров
        required_fields = ['gender', 'age_range', 'event_type', 'relationship', 'price_range']
        for field in required_fields:
            if field not in recipient_data:
                return Response(
                    {"error": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Создание графа
        graph = build_graph()

        # Создание RecommendationEngine с графом
        engine = RecommendationEngine(user_id, graph)

        recommendations = engine.get_recommendations(
            gender=recipient_data['gender'],
            age_range=recipient_data['age_range'],
            event_type=recipient_data['event_type'],
            relationship=recipient_data['relationship'],
            price_range=recipient_data['price_range'],
            top_n=3  # Количество рекомендаций
        )

        return Response({
            "recommendations": recommendations
        }, status=status.HTTP_200_OK)
