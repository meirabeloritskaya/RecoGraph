from recommendations.graph import build_graph
from recommendations.engine import RecommendationEngine
from present.models import Product


# def get_combined_recommendations(user_id, gender=None, age_range=None, event_type=None, relationship=None, k=5, top_n=3, weights=None):
def get_combined_recommendations(
    user_id, gender=None, age_range=None, k=5, top_n=3, weights=None
):
    """
    Получить персонализированные рекомендации с учетом фильтрации по параметрам.
    """
    # Создаем граф внутри функции
    graph = build_graph()

    # Устанавливаем веса по умолчанию, если они не заданы
    if weights is None:
        weights = {"knn": 3, "collaborative": 2, "pagerank": 1}

    # **ШАГ 1: Фильтруем товары по входным критериям**
    filtered_products = Product.objects.all()

    print(f"🛒 Всего товаров в БД: {filtered_products.count()}")  # 🔄 Добавлено

    print(
        "📌 Список значений gender в БД:",
        list(filtered_products.values_list("gender", flat=True)),
    )
    print(
        "📌 Список значений age_range в БД:",
        list(filtered_products.values_list("age_range", flat=True)),
    )
    # print("📌 Уникальные event_type в БД:", Product.objects.values_list("event_type", flat=True).distinct())
    # print("📌 Уникальные relationship в БД:", Product.objects.values_list("relationship", flat=True).distinct())

    # 🔄 Проверяем входные параметры перед фильтрацией
    print(f"Фильтрация по: gender={gender}, age_range={age_range}")

    if gender:
        filtered_products = filtered_products.filter(gender__contains=gender)
        print(
            f"🔍 После фильтрации gender={gender}: {filtered_products.count()} товаров"
        )

    if age_range:
        filtered_products = filtered_products.filter(age_range__contains=age_range)
        print(
            f"🔍 После фильтрации age_range={age_range}: {filtered_products.count()} товаров"
        )

    # if event_type:
    #     filtered_products = filtered_products.filter(event_type__iexact=event_type.lower())
    #     print(f"🔍 После фильтрации event_type={event_type}: {filtered_products.count()} товаров")
    #
    # if relationship:
    #     filtered_products = filtered_products.filter(relationship__iexact=relationship.lower())
    #     print(f"🔍 После фильтрации relationship={relationship}: {filtered_products.count()} товаров")

    # Преобразуем список в множество ID для удобства
    filtered_product_ids = set(filtered_products.values_list("id", flat=True))

    print(f"✅ Отфильтрованные товары (ID): {list(filtered_product_ids)}")

    if not filtered_product_ids:
        print(
            "⚠ Warning: No products passed the filtering criteria."
        )  # 🔄 Дублируем предупреждение

    # **ШАГ 2: Запускаем алгоритмы, но только по отфильтрованным товарам**
    engine = RecommendationEngine(user_id, graph)

    knn_recommendations = [
        p
        for p in engine.get_recommendations_with_knn(
            k=k, top_n=top_n, filtered_product_ids=filtered_product_ids
        )
    ]

    collaborative_recommendations = [
        p
        for p in engine.collaborative_filtering(
            top_n=top_n, filtered_product_ids=filtered_product_ids
        )
    ]

    pagerank_recommendations = [
        p
        for p in engine.get_recommendations_with_pagerank(
            top_n=top_n, filtered_product_ids=filtered_product_ids
        )
    ]

    print(f"📌 KNN recommendations: {knn_recommendations}")  # 🔄 Логирование
    print(
        f"📌 Collaborative recommendations: {collaborative_recommendations}"
    )  # 🔄 Логирование
    print(f"📌 PageRank recommendations: {pagerank_recommendations}")  # 🔄 Логирование

    # **ШАГ 3: Комбинируем результаты с учетом веса**
    recommendation_scores = {}

    for product in set(
        knn_recommendations + collaborative_recommendations + pagerank_recommendations
    ):
        score = 0
        if product in knn_recommendations:
            score += weights.get("knn", 0)
        if product in collaborative_recommendations:
            score += weights.get("collaborative", 0)
        if product in pagerank_recommendations:
            score += weights.get("pagerank", 0)
        recommendation_scores[product] = score

    # **ШАГ 4: Сортируем и берем топ-N**
    sorted_recommendations = sorted(
        recommendation_scores.items(), key=lambda x: x[1], reverse=True
    )
    top_recommendations = [product[0] for product in sorted_recommendations[:top_n]]

    print(
        f"✅ Финальные рекомендации: {top_recommendations}"
    )  # 🔄 Лог финального результата

    return top_recommendations
