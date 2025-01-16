import networkx as nx
from recommendations.models import UserInteraction
from recommendations.utils import ACTION_WEIGHTS


def build_graph():
    G = nx.Graph()

    # Добавляем узлы пользователей и товаров
    interactions = UserInteraction.objects.all()
    for interaction in interactions:
        user_node = f"user_{interaction.user.id}"
        product_node = f"product_{interaction.product.id}"

        # Добавляем узлы, если их ещё нет
        if not G.has_node(user_node):
            G.add_node(user_node, type="user")
        if not G.has_node(product_node):
            G.add_node(product_node, type="product")

        # Добавляем ребро с весом на основе действия
        weight = ACTION_WEIGHTS[interaction.action]
        G.add_edge(user_node, product_node, weight=weight)

    return G
