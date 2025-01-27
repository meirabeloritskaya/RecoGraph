from recommendations.models import UserInteraction
from recommendations.utils import ACTION_WEIGHTS


class RecommendationEngine:
    def __init__(self, user_id, graph):
        """
        Инициализация движка рекомендаций.
        :param user_id: ID пользователя
        :param graph: Граф данных
        """
        self.user_id = user_id
        self.graph = graph

    def find_similar_recipients(self, gender, age_range, event_type, relationship, price_range):
        """
        Найти получателей, похожих по возрасту, полу и хотя бы одному из дополнительных критериев.
        """
        print("Node data for recipient_8:", self.graph.nodes.get("recipient_8", "Not found"))
        print("Node data for recipient_9:", self.graph.nodes.get("recipient_9", "Not found"))
        print("\nStarting to search for similar recipients...\n")

        similar_recipients = []
        for node in self.graph.nodes:
            if self.graph.nodes[node].get('type') == 'recipient':
                gender_match = self.graph.nodes[node].get('gender') == gender
                age_range_match = self.graph.nodes[node].get('age_range') == age_range

                # Дополнительные критерии
                event_type_match = self.graph.nodes[node].get('event_type') == event_type
                relationship_match = self.graph.nodes[node].get('relationship') == relationship
                price_match = self.graph.nodes[node].get('price_range') == price_range

                # Логирование текущего узла и результатов проверки
                print(f"Checking {node}:")
                print(
                    f"  Gender Match: {gender_match} (Expected: {gender}, Actual: {self.graph.nodes[node].get('gender')})")
                print(
                    f"  Age Range Match: {age_range_match} (Expected: {age_range}, Actual: {self.graph.nodes[node].get('age_range')})")
                print(
                    f"  Event Type Match: {event_type_match} (Expected: {event_type}, Actual: {self.graph.nodes[node].get('event_type')})")
                print(
                    f"  Relationship Match: {relationship_match} (Expected: {relationship}, Actual: {self.graph.nodes[node].get('relationship')})")
                print(
                    f"  Price Match: {price_match} (Expected: {price_range}, Actual: {self.graph.nodes[node].get('price')})")

                # Добавить, если пол и возраст совпадают, и хотя бы один из дополнительных критериев
                if gender_match and age_range_match and (event_type_match or relationship_match or price_match):
                    similar_recipients.append(node)
                    print(f"  --> Added {node} as similar recipient.\n")
                else:
                    print(f"  --> {node} is not a similar recipient.\n")

        # Логирование результата
        print("\nSimilar recipients found:")
        for recipient in similar_recipients:
            print(f"  {recipient}: {self.graph.nodes[recipient]}")
        print("\nSearch completed.\n")

        return similar_recipients

    def get_related_users(self, similar_recipients):
        """
        Найти пользователей, связанных с похожими получателями.
        """
        related_users = set()
        for recipient_node in similar_recipients:
            user_node = next(
                (neighbor for neighbor in self.graph.neighbors(recipient_node)
                 if self.graph.nodes[neighbor].get('type') == 'user'),
                None
            )
            if user_node:
                related_users.add(user_node)
        return related_users

    def calculate_product_weights(self, related_user_ids):
        """
        Рассчитать веса продуктов на основе взаимодействий.
        """
        recommendations = {}
        user_interactions = UserInteraction.objects.filter(user_id__in=related_user_ids)

        for interaction in user_interactions:
            product_id = interaction.product.id
            weight = ACTION_WEIGHTS.get(interaction.action, 0)

            if product_id not in recommendations:
                recommendations[product_id] = 0
            recommendations[product_id] += weight

        return recommendations

    def get_recommendations(self, gender, age_range, event_type, relationship, price_range, top_n=3):
        """
        Основная логика генерации рекомендаций.
        """
        user_node = f"user_{self.user_id}"
        if user_node not in self.graph:
            print(f"User node {user_node} not found in graph.")
            return []

        # Найти похожих получателей
        similar_recipients = self.find_similar_recipients(gender, age_range, event_type, relationship, price_range)
        if not similar_recipients:
            print("No similar recipients found.")
            return []

        print(f"Found {len(similar_recipients)} similar recipients.")

        # Найти связанных пользователей
        related_users = self.get_related_users(similar_recipients)
        if not related_users:
            print("No related users found.")
            return []

        related_user_ids = [int(user.split('_')[1]) for user in related_users]

        # Рассчитать веса продуктов
        recommendations = self.calculate_product_weights(related_user_ids)

        # Ранжировать продукты
        sorted_recommendations = sorted(
            recommendations.items(), key=lambda x: x[1], reverse=True
        )

        # Возврат топ-N продуктов
        return [
            self.graph.nodes[f"product_{product_id}"].get('product')
            for product_id, _ in sorted_recommendations[:top_n]
        ]
