from django.core.management.base import BaseCommand
from recommendations.graph import build_graph


class Command(BaseCommand):
    help = "Rebuilds the recommendation graph"

    def handle(self, *args, **options):
        graph = build_graph()
        self.stdout.write("Graph rebuilt successfully!")
        self.stdout.write(f"Graph nodes: {graph.nodes(data=True)}")
        self.stdout.write(f"Graph edges: {graph.edges(data=True)}")
