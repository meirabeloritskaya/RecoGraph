import json
from django.core.management.base import BaseCommand
from present.models import Category, Product  # Убедитесь, что это ваши модели


class Command(BaseCommand):
    help = 'Import categories and products from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = 'present/data/products.json'

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found"))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Invalid JSON format in {file_path}"))
            return

        for category_data in data['categories']:
            # Создание категории
            category, created = Category.objects.get_or_create(name=category_data['name'])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category '{category.name}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"Category '{category.name}' already exists"))

            # Создание продуктов для категории
            for product_data in category_data['products']:
                Product.objects.create(
                    category=category,
                    name=product_data['name'],
                    gender=product_data['gender'],
                    age_range=product_data['age_range'],
                    description=product_data['description'],
                    price=product_data['price'],
                    in_stock=product_data['in_stock'],
                )
                self.stdout.write(self.style.SUCCESS(f"Product '{product_data['name']}' created in category '{category.name}'"))

        self.stdout.write(self.style.SUCCESS("Categories and products imported successfully!"))
