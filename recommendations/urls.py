from django.urls import path
from recommendations.views import RecommendationsView, UserActionView


app_name = 'recommendations'

urlpatterns = [
    path('actions/<str:action>/', UserActionView.as_view(), name='user_action'),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
]
