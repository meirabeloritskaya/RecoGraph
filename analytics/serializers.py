from analytics.models import ProductAnalytics
from rest_framework import serializers
from present.models import Product


class ProductSerializer(serializers.ModelSerializer):
    analytics = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'analytics']

    def get_analytics(self, obj):
        analytics = getattr(obj, 'analytics', None)
        if analytics:
            return {
                'views_count': analytics.views_count,
                'favorites_count': analytics.favorites_count,
                'purchases_count': analytics.purchases_count,
            }
        return None
