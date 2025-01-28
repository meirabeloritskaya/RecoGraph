from django.core.management.base import BaseCommand
from recommendations.graph import build_graph
from present.models import Product


class Command(BaseCommand):
    help = "Тестирование рекомендаций на основе PageRank"

    def handle(self, *args, **kwargs):
        self.stdout.write("Создаем граф...\n")
        graph = build_graph()

        self.stdout.write("\nPageRank scores calculated:\n")
        for node, data in graph.nodes(data=True):
            pagerank = data.get('pagerank', 0)
            self.stdout.write(f"{node}: PageRank = {pagerank}")

        self.stdout.write("\nТестируем рекомендации на основе PageRank...\n")
        # Отбираем узлы продуктов
        product_nodes = [
            (node, data['pagerank'])
            for node, data in graph.nodes(data=True)
            if data.get('type') == 'product'
        ]

        # Сортируем продукты по PageRank
        sorted_products = sorted(product_nodes, key=lambda x: x[1], reverse=True)

        # Берем топ-N продуктов
        top_n = 3
        top_products = [
            Product.objects.get(id=int(node.split('_')[1]))
            for node, _ in sorted_products[:top_n]
        ]

        # Выводим результаты
        if top_products:
            self.stdout.write("\nРекомендации на основе PageRank:")
            for product in top_products:
                self.stdout.write(f"- {product.name} (ID: {product.id})")
        else:
            self.stdout.write("Нет продуктов для рекомендаций.")
