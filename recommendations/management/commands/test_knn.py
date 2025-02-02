from django.core.management.base import BaseCommand
from recommendations.engine import RecommendationEngine
from recommendations.graph import build_graph


class Command(BaseCommand):
    help = "Тестирование k-NN рекомендаций"

    def handle(self, *args, **kwargs):
        user_id = 8  # Укажите ID пользователя для теста
        k = 5  # Количество соседей
        top_n = 3  # Количество рекомендаций

        # Создаем граф
        self.stdout.write("Создаем граф...")
        graph = build_graph()
        self.stdout.write("Граф успешно создан.\n")

        # Создаем экземпляр RecommendationEngine
        engine = RecommendationEngine(user_id, graph)

        # Тестируем k-NN рекомендации
        self.stdout.write(
            f"Тестирование k-NN для пользователя {user_id}, k={k}, top_n={top_n}...\n"
        )
        recommendations = engine.get_recommendations_with_knn(k=k, top_n=top_n)

        # Вывод результатов
        if recommendations:
            self.stdout.write("Рекомендации:")
            for product in recommendations:
                self.stdout.write(f"- {product.name} (ID: {product.id})")
        else:
            self.stdout.write("Нет рекомендаций.")
