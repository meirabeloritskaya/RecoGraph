from recommendations.models import UserInteraction, Product
from rest_framework import status
from rest_framework.response import Response


class UserActionHandler:
    def __init__(self, user, product_id):
        self.user = user
        self.product_id = product_id
        self.product = self.get_product()

    def get_product(self):
        try:
            return Product.objects.get(id=self.product_id)
        except Product.DoesNotExist:
            return None

    def handle_action(self, action):
        if not self.product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Создаём или обновляем взаимодействие
        interaction, created = UserInteraction.objects.get_or_create(
            user=self.user,
            product_id=self.product_id,
            defaults={'action': action}
        )

        if not created and interaction.action != action:
            interaction.action = action
            interaction.save()

        response_data = {
            "message": f"Successfully marked as {action}" if created else f"Action updated to {action}",
            "product_name": self.product.name,
            "price": f"{self.product.price} {self.product.get_currency_display()}"
        }

        return Response(response_data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


def add_to_favorites(user, product_id):
    handler = UserActionHandler(user, product_id)
    return handler.handle_action('favorite')


def add_to_cart(user, product_id):
    handler = UserActionHandler(user, product_id)
    return handler.handle_action('cart')


def mark_as_viewed(user, product_id):
    handler = UserActionHandler(user, product_id)
    return handler.handle_action('view')


def mark_as_bought(user, product_id):
    handler = UserActionHandler(user, product_id)
    return handler.handle_action('buy')
