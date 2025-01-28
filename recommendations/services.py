from recommendations.graph import build_graph
from recommendations.engine import RecommendationEngine

def get_combined_recommendations(user_id, k=5, top_n=3, weights=None):
    """
    Получить объединенные рекомендации, используя k-NN, коллаборативную фильтрацию и PageRank.
    :param user_id: ID пользователя
    :param k: Количество соседей для k-NN
    :param top_n: Количество рекомендаций
    :param weights: Веса для методов: {"knn": 3, "collaborative": 2, "pagerank": 1}
    :return: Список объектов Product
    """
    # Создаем граф внутри функции
    graph = build_graph()

    # Устанавливаем веса по умолчанию, если они не заданы
    if weights is None:
        weights = {"knn": 3, "collaborative": 2, "pagerank": 1}

    # Создаем экземпляр RecommendationEngine
    engine = RecommendationEngine(user_id, graph)

    # Получаем рекомендации из всех методов
    knn_recommendations = engine.get_recommendations_with_knn(k=k, top_n=top_n)
    collaborative_recommendations = engine.collaborative_filtering(top_n=top_n)
    pagerank_recommendations = engine.get_recommendations_with_pagerank(top_n=top_n)

    # Объединяем результаты и вычисляем общий вес
    recommendation_scores = {}
    for product in set(knn_recommendations + collaborative_recommendations + pagerank_recommendations):
        score = 0
        if product in knn_recommendations:
            score += weights.get("knn", 0)
        if product in collaborative_recommendations:
            score += weights.get("collaborative", 0)
        if product in pagerank_recommendations:
            score += weights.get("pagerank", 0)
        recommendation_scores[product] = score

    # Сортируем рекомендации по их общему весу
    sorted_recommendations = sorted(
        recommendation_scores.items(), key=lambda x: x[1], reverse=True
    )

    # Берем только топ-N
    top_recommendations = [product[0] for product in sorted_recommendations[:top_n]]

    return top_recommendations
