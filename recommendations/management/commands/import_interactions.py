import json
from recommendations.models import UserInteraction
from django.contrib.auth import get_user_model
from present.models import Product
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load interactions from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing interactions')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for interaction in data['interactions']:
            user = get_user_model().objects.get(id=interaction['user_id'])
            product = Product.objects.get(id=interaction['product_id'])
            action = interaction['action']

            UserInteraction.objects.create(user=user, product=product, action=action)

        self.stdout.write(self.style.SUCCESS("Interactions loaded successfully!"))
