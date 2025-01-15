 
import json
from django.core.management.base import BaseCommand
from present.models import Category, Product


class Command(BaseCommand):
    help = 'Import categories and products from JSON file'

    def handle(self, *args, **kwargs):

        file_path = 'present/data/products.json'

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                for category_data in data['categories']:
                    category, created = Category.objects.get_or_create(
                        name=category_data['name']
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Category "{category.name}" created'))

                    for product_data in category_data['products']:
                        Product.objects.get_or_create(
                            name=product_data['name'],
                            category=category,
                            defaults={
                                'price': product_data['price'],
                                'in_stock': product_data['in_stock'],
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f'Product "{product_data["name"]}" added to category "{category.name}"'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please check the path.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format.'))
