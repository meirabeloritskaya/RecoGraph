from django.urls import path
from recommendations.views import (
    RecommendationsView,
    UserActionView,
    RecommendationResultsView,
)


app_name = "recommendations"

urlpatterns = [
    path("actions/<str:action>/", UserActionView.as_view(), name="user_action"),
    path("", RecommendationsView.as_view(), name="recommendations"),
    path("results/", RecommendationResultsView.as_view(), name="results"),
]
