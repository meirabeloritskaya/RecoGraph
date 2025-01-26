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
            return []

        if not list(self.graph.neighbors(user_node)):
            print(f"User {user_node} has no interactions.")
            return []

        recommendations = []
        for node in self.graph.nodes:
            if self.graph.nodes[node].get('type') == 'product':
                product = self.graph.nodes[node]['product']

                if gender in product.gender and age_range in product.age_range:
                    if (
                        getattr(product, 'event_type', None) == event_type or
                        getattr(product, 'relationship', None) == relationship or
                        getattr(product, 'price', None) == price
                    ):
                        edge_data = self.graph.get_edge_data(user_node, node)
                        weight = edge_data.get('weight', 0) if edge_data else 0
                        recommendations.append((node, weight))

        recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

        return [
            self.graph.nodes[node].get('product')
            for node, _ in recommendations[:top_n]
            if 'product' in self.graph.nodes[node]
        ]
