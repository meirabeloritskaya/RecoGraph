import networkx as nx
from recommendations.models import UserInteraction
from recipients.models import Recipients
from recommendations.utils import ACTION_WEIGHTS


def build_graph():
    G = nx.Graph()

    # 1. Создаем узлы пользователей и их получателей
    recipients = Recipients.objects.select_related('user')
    for recipient in recipients:
        user_node = f"user_{recipient.user.id}"
        recipient_node = f"recipient_{recipient.id}"

        G.add_node(user_node, type="user")
        G.add_node(recipient_node, type="recipient")

        G.add_edge(user_node, recipient_node)

    # 2. Создаем узлы продуктов и добавляем взаимодействия
    interactions = UserInteraction.objects.select_related('user', 'product')
    for interaction in interactions:
        product_node = f"product_{interaction.product.id}"
        G.add_node(product_node, type="product", product=interaction.product)

        user_recipients = interaction.user.recipients.all()
        weight = ACTION_WEIGHTS[interaction.action]
        for rec in user_recipients:
            recipient_node = f"recipient_{rec.id}"
            G.add_edge(recipient_node, product_node, weight=weight)

    # 3. Вычисляем PageRank
    pagerank_scores = nx.pagerank(G)
    for node, rank in pagerank_scores.items():
        G.nodes[node]['pagerank'] = rank

    print("\nPageRank scores calculated:")
    for node, data in G.nodes(data=True):
        print(f"{node}: {data.get('pagerank', 0)}")

    return G
