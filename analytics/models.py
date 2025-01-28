from django.db import models
from django.utils.timezone import now
from present.models import Product


class ProductAnalytics(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="analytics")
    views_count = models.PositiveIntegerField(default=0)
    favorites_count = models.PositiveIntegerField(default=0)
    purchases_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(default=now)

    def __str__(self):
        return f"Analytics for {self.product.name}"
