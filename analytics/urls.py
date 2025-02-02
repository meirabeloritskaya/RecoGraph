from django.urls import path
from .views import TopProductsView, UserActionsStatsView, SummaryAnalyticsView

urlpatterns = [
    path("top-products/", TopProductsView.as_view(), name="top-products"),
    path("user-actions/", UserActionsStatsView.as_view(), name="user-actions"),
    path("summary/", SummaryAnalyticsView.as_view(), name="summary-analytics"),
]
