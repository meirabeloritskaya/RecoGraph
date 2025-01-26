import json
from django.core.management.base import BaseCommand
from present.models import Category, Product


class Command(BaseCommand):
    help = 'Import products from JSON file'

    def handle(self, *args, **kwargs):

        file_path = 'present/data/products.json'

        # Определяем диапазоны цен
        def get_price_range(price):
            if 100 <= price <= 1500:
                return '100-1500'
            elif 1501 <= price <= 5000:
                return '1501-5000'
            elif 5001 <= price <= 10000:
                return '5001-10000'
            elif 10001 <= price <= 50000:
                return '10001-50000'
            elif 50001 <= price <= 100000:
                return '50001-100000'
            elif 100001 <= price <= 200000:
                return '100001-200000'
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                for category_data in data['categories']:
                    # Создаём или получаем категорию
                    category, created = Category.objects.get_or_create(
                        name=category_data['name']
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Category "{category.name}" created'))

                    # Обрабатываем товары в категории
                    for product_data in category_data['products']:
                        # Определяем диапазон цен
                        price_range = get_price_range(product_data['price'])
                        if price_range is None:
                            self.stdout.write(self.style.WARNING(
                                f"Price {product_data['price']} for product '{product_data['name']}' is out of range. Skipping."
                            ))
                            continue

                        # Создаём или обновляем продукт
                        Product.objects.get_or_create(
                            name=product_data['name'],
                            category=category,
                            defaults={
                                'price': product_data['price'],
                                'price_range': price_range,
                                'in_stock': product_data['in_stock'],
                                'gender': product_data.get('gender', None),
                                'age_range': product_data.get('age_range', None),
                                'description': product_data.get('description', ''),
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(
                            f'Product "{product_data["name"]}" added to category "{category.name}" with price range {price_range}'
                        ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please check the path.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format.'))
