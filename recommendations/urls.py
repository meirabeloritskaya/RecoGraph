from django.urls import path
from recommendations.views import (
    AddToFavoriteView,
    AddToCartView,
    MarkAsViewedView,
    MarkAsBoughtView,
    RecommendationsView
)

app_name = 'recommendations'

urlpatterns = [
    path('interactions/add-to-favorites/', AddToFavoriteView.as_view(), name='add_to_favorites'),
    path('interactions/add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('interactions/mark-as-viewed/', MarkAsViewedView.as_view(), name='mark_as_viewed'),
    path('interactions/mark-as-bought/', MarkAsBoughtView.as_view(), name='mark_as_bought'),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
]
