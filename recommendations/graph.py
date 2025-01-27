import networkx as nx
from recommendations.models import UserInteraction
from recipients.models import Recipients
from recommendations.utils import ACTION_WEIGHTS


def build_graph():
    G = nx.Graph()

    # 1) Сначала обрабатываем всех получателей и их пользователей,
    #    чтобы создать узлы user_<id> и recipient_<id>, а также связь между ними.
    recipients = Recipients.objects.select_related('user')
    for recipient in recipients:
        user_node = f"user_{recipient.user.id}"
        recipient_node = f"recipient_{recipient.id}"

        # Добавляем узел пользователя
        G.add_node(user_node, type="user")
        print(f"Added user node: {user_node}, type: user")

        # Добавляем узел получателя
        G.add_node(recipient_node,
            type="recipient",
            gender=recipient.gender,
            age_range=recipient.age_range,
            event_type=recipient.event_type,
            relationship=recipient.relationship,
            price_range=recipient.price_range,)

        print(f"Added recipient node: {recipient_node}, attributes: {{"
              f"'gender': {recipient.gender}, 'age_range': {recipient.age_range}, "
              f"'event_type': {recipient.event_type}, 'relationship': {recipient.relationship}, "
              f"'price_range': {recipient.price_range}}}")

        # Связь между пользователем и получателем (без веса или с весом=0)
        G.add_edge(user_node, recipient_node)
        print(f"Added edge user->recipient: {user_node} -> {recipient_node}")

    # 2) Теперь обрабатываем взаимодействия (UserInteraction), чтобы
    #    создать/добавить узлы продуктов и связать их с получателями.
    interactions = UserInteraction.objects.select_related('user', 'product')
    for interaction in interactions:
        product_node = f"product_{interaction.product.id}"

        # Добавляем/обновляем узел продукта с нужными атрибутами
        G.add_node(
            product_node,
            type="product",
            product=interaction.product,
            product_id=interaction.product.id,
            name=interaction.product.name,
            gender=interaction.product.gender,
            age_range=interaction.product.age_range,
            event_type=getattr(interaction.product, "event_type", None),
            relationship=getattr(interaction.product, "relationship", None),
            price=interaction.product.price,
            price_range=interaction.product.price_range,
        )

        print(f"Added/updated product node: {product_node}, attributes: {interaction.product}")

        # Для каждого получателя, принадлежащего этому пользователю
        user_recipients = interaction.user.recipients.all()
        if not user_recipients:
            print(f"Skipping user {interaction.user.id}, no recipients found.")
            continue

        # Создаем связи recipient_<id> -> product_<id> с весом
        weight = ACTION_WEIGHTS[interaction.action]
        for rec in user_recipients:
            recipient_node = f"recipient_{rec.id}"

            if rec.gender in interaction.product.gender or "male" in interaction.product.gender and "female" in interaction.product.gender:
                G.add_edge(recipient_node, product_node, weight=weight)
                print(f"Added edge: {recipient_node} -> {product_node}, weight: {weight}")
            else:
                print(f"Skipping product {product_node} for recipient {recipient_node}: gender mismatch")

    return G

