import numpy as np
from recommendations.models import UserInteraction
from sklearn.metrics.pairwise import cosine_similarity

# Веса действий пользователей
ACTION_WEIGHTS = {
    "view": 1,  # Просмотрено
    "favorite": 2,  # Добавлено в избранное
    "cart": 3,  # Добавлено в корзину
    "buy": 4,  # Куплено
}


def build_interaction_matrix(filtered_product_ids=None):
    """
    Строит матрицу взаимодействий пользователей с продуктами.
    """
    interactions = UserInteraction.objects.select_related("user", "product")

    # Если передан список ID товаров, оставляем только их
    if filtered_product_ids is not None:
        interactions = interactions.filter(product_id__in=filtered_product_ids)

    users = {interaction.user.id for interaction in interactions}
    products = {interaction.product.id for interaction in interactions}

    user_index = {user_id: idx for idx, user_id in enumerate(users)}
    product_index = {product_id: idx for idx, product_id in enumerate(products)}

    # Инициализируем матрицу
    interaction_matrix = np.zeros((len(users), len(products)))

    for interaction in interactions:
        user_idx = user_index[interaction.user.id]
        product_idx = product_index[interaction.product.id]
        weight = ACTION_WEIGHTS.get(interaction.action, 0)
        interaction_matrix[user_idx, product_idx] += weight

    return interaction_matrix, user_index, product_index


def calculate_user_similarity(interaction_matrix):
    """
    Вычисляет косинусное сходство между пользователями.
    """
    return cosine_similarity(interaction_matrix)


def find_nearest_neighbors(user_id, user_index, similarity_matrix, k=5):
    """
    Находит k ближайших соседей для заданного пользователя.
    """
    if user_id not in user_index:
        return []

    user_idx = user_index[user_id]
    similarities = similarity_matrix[user_idx]

    # Найти индексы топ-k самых похожих пользователей
    similar_users = np.argsort(-similarities)[
        1 : k + 1
    ]  # Исключаем самого пользователя (сходство = 1)
    return [user for user, idx in user_index.items() if idx in similar_users]
