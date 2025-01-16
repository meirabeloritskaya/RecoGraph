from .graph import build_graph


class RecommendationEngine:
    def __init__(self, user_id):
        self.user_id = user_id
        self.graph = build_graph()

    def get_recommendations(self):
        user_node = f"user_{self.user_id}"

        if user_node not in self.graph:
            return []  # Если пользователь не взаимодействовал с продуктами, возвращаем пусто

        # Получаем все соседние узлы (товары)
        neighbors = self.graph.neighbors(user_node)

        # Сортируем товары по весу (важности взаимодействия)
        recommendations = sorted(
            neighbors,
            key=lambda n: self.graph[user_node][n]['weight'],
            reverse=True
        )

        # Фильтруем только продукты
        product_recommendations = [n for n in recommendations if n.startswith("product_")]

        return product_recommendations

    def get_top_n_recommendations(self, n=3):
        """
        Возвращает топ N рекомендаций для пользователя.
        """
        all_recommendations = self.get_recommendations()
        return all_recommendations[:n]  # Берём первые N рекомендаций