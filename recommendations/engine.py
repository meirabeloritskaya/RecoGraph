from .graph import build_graph


class RecommendationEngine:
    def __init__(self, user_id):
        """
        Инициализация движка рекомендаций для пользователя.
        :param user_id: ID пользователя
        """
        self.user_id = user_id
        self.graph = build_graph()

    def get_recommendations(self, gender, age_range, event_type, relationship, price, top_n=3):
        user_node = f"user_{self.user_id}"

        if user_node not in self.graph:
            print(f"User node {user_node} not found in graph.")
            return []  # Если пользователь не взаимодействовал с продуктами, возвращаем пусто

        # Вывод всех узлов графа для проверки
        print("Graph nodes:", self.graph.nodes(data=True))

        # Фильтрация узлов, соответствующих указанным параметрам
        recommendations = []
        for node in self.graph.nodes:
            if self.graph.nodes[node].get('type') == 'product':
                product = self.graph.nodes[node]['product']
                print(f"Checking product node: {node}, attributes: {product}")

                print(f"Product: {product}, Gender: {product.gender}, Age Range: {product.age_range}")

                if product.gender == gender and product.age_range == age_range:
                    print(f"Product passed gender and age range filter: {product}")
                    # Проверяем дополнительные параметры (с логикой ИЛИ)
                    if (
                            product.event_type == event_type or
                            product.relationship == relationship or
                            product.price == price
                    ):
                        print(f"Product passed additional filters: {product}")
                        edge_data = self.graph.get_edge_data(user_node, node)
                        if edge_data and 'weight' in edge_data:
                            recommendations.append((node, edge_data['weight']))
                            print(f"Matched product: {node} with weight: {edge_data['weight']}")

        # Сортируем рекомендации по весу
        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
        print("Filtered recommendations:", recommendations)

        # Возвращаем топ N рекомендаций
        return [self.graph.nodes[node]['product'] for node, _ in recommendations[:top_n]]

