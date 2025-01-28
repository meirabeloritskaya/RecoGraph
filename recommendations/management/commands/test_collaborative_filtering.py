from django.core.management.base import BaseCommand
from recommendations.graph import build_graph
from recommendations.engine import RecommendationEngine


class Command(BaseCommand):
    help = "Тестирование коллаборативной фильтрации"

    def handle(self, *args, **kwargs):
        user_id = 8  # Укажите ID пользователя для теста
        top_n = 3  # Количество рекомендаций
        engine = RecommendationEngine(user_id, graph=build_graph())

        print(f"Тестирование коллаборативной фильтрации для пользователя {user_id}, top_n={top_n}...\n")
        recommendations = engine.collaborative_filtering(top_n=top_n)

        if recommendations:
            print("Рекомендации:")
            for product in recommendations:
                print(f"- {product.name} (ID: {product.id})")
        else:
            print("Нет рекомендаций.")
