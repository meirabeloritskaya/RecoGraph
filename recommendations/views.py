
from rest_framework.views import APIView
from recommendations.actions import add_to_favorites, add_to_cart, mark_as_viewed, mark_as_bought
from recommendations.engine import RecommendationEngine
from rest_framework.response import Response
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
        Принимает параметры получателя и возвращает рекомендации (метод POST).
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

    def get(self, request):
        """
        Принимает параметры через query string и возвращает рекомендации (метод GET).
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "user_id is required as a query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Параметры получателя из query string
        gender = request.query_params.get('gender')
        age_range = request.query_params.get('age_range')
        event_type = request.query_params.get('event_type')
        relationship = request.query_params.get('relationship')
        price = request.query_params.get('price')

        # Проверяем наличие обязательных параметров
        if not all([gender, age_range, event_type, relationship, price]):
            return Response(
                {"error": "All parameters (gender, age_range, event_type, relationship, price) are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем рекомендации
        engine = RecommendationEngine(user_id)
        recommendations = engine.get_recommendations(
            gender=gender,
            age_range=age_range,
            event_type=event_type,
            relationship=relationship,
            price=price,
            top_n=3  # Количество рекомендаций
        )

        return Response({
            "recommendations": recommendations
        }, status=status.HTTP_200_OK)
