from recommendations.utils import build_interaction_matrix, calculate_user_similarity, find_nearest_neighbors
import numpy as np
from present.models import Product
from recommendations.utils import build_interaction_matrix, calculate_user_similarity


class RecommendationEngine:
    def __init__(self, user_id, graph):
        self.user_id = user_id
        self.graph = graph

    # Существующие методы (например, calculate_product_weights)

    def get_recommendations_with_knn(self, k=5, top_n=3):
        """
        Генерация рекомендаций с использованием k-NN.
        """
        # Построить матрицу взаимодействий
        interaction_matrix, user_index, product_index = build_interaction_matrix()

        # Вычислить сходство пользователей
        similarity_matrix = calculate_user_similarity(interaction_matrix)

        # Найти ближайших соседей
        neighbors = find_nearest_neighbors(self.user_id, user_index, similarity_matrix, k)
        if not neighbors:
            print("No similar users found.")
            return []

        # Собрать все продукты, с которыми взаимодействовали соседи
        neighbor_indices = [user_index[neighbor] for neighbor in neighbors]
        product_scores = np.sum(interaction_matrix[neighbor_indices], axis=0)

        # Отсортировать продукты по убыванию их популярности среди соседей
        top_products_indices = np.argsort(-product_scores)[:top_n]
        product_ids = [product for product, idx in product_index.items() if idx in top_products_indices]

        # Вернуть объекты продуктов
        return [Product.objects.get(id=product_id) for product_id in product_ids]

    def collaborative_filtering(self, top_n=3, k=5):
        """
        Реализация коллаборативной фильтрации (user-based).
        :param top_n: Количество рекомендаций.
        :param k: Количество ближайших пользователей.
        """
        # Построить матрицу взаимодействий
        interaction_matrix, user_index, product_index = build_interaction_matrix()

        # Проверить, есть ли пользователь в матрице
        if self.user_id not in user_index:
            print(f"User {self.user_id} not found in interaction matrix.")
            return []

        # Вычислить сходство пользователей
        similarity_matrix = calculate_user_similarity(interaction_matrix)

        # Найти индекс текущего пользователя
        target_user_idx = user_index[self.user_id]

        # Найти k наиболее схожих пользователей
        user_similarities = similarity_matrix[target_user_idx]
        similar_users = np.argsort(-user_similarities)[:k]

        # Собрать продукты, с которыми взаимодействовали схожие пользователи
        recommended_scores = np.zeros(interaction_matrix.shape[1])
        for user_idx in similar_users:
            if user_idx != target_user_idx:
                recommended_scores += interaction_matrix[user_idx]

        # Убрать продукты, с которыми уже взаимодействовал целевой пользователь
        user_interactions = interaction_matrix[target_user_idx]
        recommended_scores = np.where(user_interactions == 0, recommended_scores, 0)

        # Найти топ-N продуктов
        top_product_indices = np.argsort(-recommended_scores)[:top_n]
        product_ids = [product for product, idx in product_index.items() if idx in top_product_indices]

        # Вернуть объекты продуктов
        return [Product.objects.get(id=product_id) for product_id in product_ids]

    def get_recommendations_with_pagerank(self, top_n=3):
        """
        Получить рекомендации на основе PageRank.
        :param top_n: Количество рекомендаций.
        :return: Список объектов Product.
        """
        # Извлечь все узлы типа 'product' и отсортировать их по PageRank
        product_nodes = [
            node for node, data in self.graph.nodes(data=True)
            if data.get('type') == 'product'
        ]

        # Сортируем узлы продуктов по значению PageRank
        sorted_products = sorted(
            product_nodes,
            key=lambda node: self.graph.nodes[node].get('pagerank', 0),
            reverse=True
        )

        # Извлекаем ID продуктов
        product_ids = [
            self.graph.nodes[node]['product'].id for node in sorted_products[:top_n]
        ]

        # Возвращаем объекты продуктов
        return [Product.objects.get(id=product_id) for product_id in product_ids]
