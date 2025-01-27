from django.core.management.base import BaseCommand
from recommendations.graph import build_graph
from recommendations.engine import RecommendationEngine


class Command(BaseCommand):
    help = "Тестирование работы рекомендаций для пользователя."

    def handle(self, *args, **kwargs):
        user_id = 8  # Задаем ID пользователя для теста
        recipient_data = {
            "gender": "male",
            "age_range": "26-50",
            "event_type": "anniversary",
            "relationship": "brother",
            "price_range": "10001-50000"
        }

        self.stdout.write(f"Testing recommendations for user_id={user_id} and recipient_data={recipient_data}")

        # Построение графа
        self.stdout.write("\nBuilding graph...")
        graph = build_graph()

        # Инициализация движка рекомендаций
        engine = RecommendationEngine(user_id, graph)

        # Получение рекомендаций
        self.stdout.write("\nFinding recommendations...")
        recommendations = engine.get_recommendations(
            gender=recipient_data["gender"],
            age_range=recipient_data["age_range"],
            event_type=recipient_data["event_type"],
            relationship=recipient_data["relationship"],
            price_range=recipient_data["price_range"]
        )

        # Вывод рекомендаций
        if recommendations:
            self.stdout.write("\nTop Recommendations:")
            for product in recommendations:
                self.stdout.write(f"- {product.name} (ID: {product.id})")
        else:
            self.stdout.write("\nNo recommendations found.")
