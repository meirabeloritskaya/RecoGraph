from django.db import models
from django.conf import settings
from present.models import Product


class UserInteraction(models.Model):
    ACTION_CHOICES = [
        ("view", "Просмотрено"),
        ("favorite", "Добавлено в избранное"),
        ("cart", "Добавлено в корзину"),
        ("buy", "Куплено"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="interactions"
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def product_price(self):
        """Возвращает цену продукта с символом валюты."""
        if self.product and self.product.price:
            return f"{self.product.price} {self.product.get_currency_display()}"
        return "No price available"

    product_price.short_description = "Цена продукта"

    def __str__(self):
        return f"{self.user} {self.action} {self.product}"
