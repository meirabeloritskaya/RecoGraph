
from rest_framework.views import APIView
from recommendations.actions import add_to_favorites, add_to_cart, mark_as_viewed, mark_as_bought
from recommendations.engine import RecommendationEngine
from rest_framework.response import Response


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
    def get(self, request):
        user_id = request.user.id
        engine = RecommendationEngine(user_id)

        recommendations = engine.get_top_n_recommendations(n=3)

        return Response({
            "recommendations": recommendations
        })
