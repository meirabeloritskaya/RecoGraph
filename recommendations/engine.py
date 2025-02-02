from recommendations.utils import find_nearest_neighbors
import numpy as np
from present.models import Product
from recommendations.utils import build_interaction_matrix, calculate_user_similarity


class RecommendationEngine:
    def __init__(self, user_id, graph):
        self.user_id = user_id
        self.graph = graph

    # Существующие методы (например, calculate_product_weights)

    def get_recommendations_with_knn(self, k=5, top_n=3, filtered_product_ids=None):
        """
        Генерация рекомендаций с использованием k-NN.
        :param k: Количество ближайших соседей
        :param top_n: Количество товаров в итоговом списке
        :param filtered_product_ids: Список ID товаров, подходящих по критериям
        """
        # Проверяем, есть ли вообще отфильтрованные товары
        if not filtered_product_ids:
            print("⚠ Warning: No products passed the filtering criteria.")
            return []

        # Построить матрицу взаимодействий только для нужных товаров
        interaction_matrix, user_index, product_index = build_interaction_matrix(
            filtered_product_ids
        )

        # Проверяем, есть ли пользователь в индексе
        if self.user_id not in user_index:
            print(f"⚠ User {self.user_id} not found in interaction matrix.")
            return []

        # Вычислить сходство пользователей
        similarity_matrix = calculate_user_similarity(interaction_matrix)

        # Найти ближайших соседей
        neighbors = find_nearest_neighbors(
            self.user_id, user_index, similarity_matrix, k
        )
        if not neighbors:
            print("⚠ No similar users found.")
            return []

        # Собрать все продукты, с которыми взаимодействовали соседи
        neighbor_indices = [user_index[neighbor] for neighbor in neighbors]
        product_scores = np.sum(interaction_matrix[neighbor_indices], axis=0)

        # Отсортировать продукты по убыванию их популярности среди соседей
        top_products_indices = np.argsort(-product_scores)

        # Фильтруем товары: оставляем только те, что прошли `filtered_product_ids`
        filtered_indices = [
            idx
            for idx in top_products_indices
            if idx
            in {
                product_index.get(pid)
                for pid in filtered_product_ids
                if pid in product_index
            }
        ]

        # Ограничиваем до `top_n`
        top_filtered_indices = filtered_indices[:top_n]

        # Получаем ID товаров, которые прошли финальную фильтрацию
        product_ids = [
            product
            for product, idx in product_index.items()
            if idx in top_filtered_indices
        ]

        # Вернуть объекты продуктов
        return [Product.objects.get(id=product_id) for product_id in product_ids]

    def collaborative_filtering(self, top_n=3, k=5, filtered_product_ids=None):
        """
        Реализация коллаборативной фильтрации (user-based).
        :param top_n: Количество рекомендаций.
        :param k: Количество ближайших пользователей.
        :param filtered_product_ids: Список ID товаров, подходящих по критериям (пол, возраст, отношения, событие).
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
        top_product_indices = np.argsort(-recommended_scores)

        # Оставляем только товары из `filtered_product_ids`
        filtered_indices = [
            idx
            for idx in top_product_indices
            if idx
            in {
                product_index.get(pid)
                for pid in filtered_product_ids
                if pid in product_index
            }
        ]

        if not filtered_indices:
            print(
                "No products matched after filtering by gender, age, relationship, and event."
            )
            return []

        # Ограничиваем до top_n
        top_filtered_indices = filtered_indices[:top_n]

        product_ids = [
            product
            for product, idx in product_index.items()
            if idx in top_filtered_indices
        ]

        # Вернуть объекты продуктов
        return [Product.objects.get(id=product_id) for product_id in product_ids]

    def get_recommendations_with_pagerank(self, top_n=3, filtered_product_ids=None):
        """
        Получить рекомендации на основе PageRank.
        :param top_n: Количество рекомендаций.
        :param filtered_product_ids: Список ID товаров, подходящих по критериям.
        :return: Список объектов Product.
        """
        # Проверяем, есть ли вообще отфильтрованные товары
        if not filtered_product_ids:
            print("⚠ Warning: No products passed the filtering criteria.")
            return []

        # Извлекаем все узлы продуктов и фильтруем по `filtered_product_ids`
        product_nodes = [
            node
            for node, data in self.graph.nodes(data=True)
            if data.get("type") == "product"
            and data.get("product")
            and data["product"].id in filtered_product_ids
        ]

        # Проверяем, есть ли продукты после фильтрации
        if not product_nodes:
            print("⚠ Warning: No products left after filtering.")
            return []

        # Сортируем узлы продуктов по значению PageRank
        sorted_products = sorted(
            product_nodes,
            key=lambda node: self.graph.nodes[node].get("pagerank", 0),
            reverse=True,
        )

        # Извлекаем ID товаров
        product_ids = [
            self.graph.nodes[node]["product"].id for node in sorted_products[:top_n]
        ]

        # Возвращаем объекты продуктов
        return [Product.objects.get(id=product_id) for product_id in product_ids]
