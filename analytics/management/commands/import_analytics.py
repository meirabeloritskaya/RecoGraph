from django.core.management.base import BaseCommand
from analytics.models import ProductAnalytics
from present.models import Product
from recommendations.models import UserInteraction
from django.db.models import Count
from django.utils.timezone import now


class Command(BaseCommand):
    help = "Заполнить аналитические данные для продуктов"

    def handle(self, *args, **kwargs):
        for product in Product.objects.all():
            interactions = UserInteraction.objects.filter(product=product)
            views = interactions.filter(action="view").count()
            favorites = interactions.filter(action="favorite").count()
            purchases = interactions.filter(action="buy").count()

            analytics, created = ProductAnalytics.objects.update_or_create(
                product=product,
                defaults={
                    "views_count": views,
                    "favorites_count": favorites,
                    "purchases_count": purchases,
                    "last_updated": now(),
                },
            )
            self.stdout.write(
                f"{'Created' if created else 'Updated'} analytics for {product.name}"
            )
