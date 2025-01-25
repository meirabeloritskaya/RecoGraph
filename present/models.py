from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    class Meta:
        ordering = ['name']  # Сортировка по имени категории

    def __str__(self):
        return self.name


class Product(models.Model):
    CURRENCY_CHOICES = [
        ('USD', '$'),  # Dollar
        ('EUR', '€'),  # Euro
        ('RUB', '₽'),  # Russian Ruble
    ]

    GENDER_CHOICES = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    ]

    AGE_RANGE_CHOICES = [
        (0, '0-1'),
        (2, '2-6'),
        (7, '7-13'),
        (14, '14-25'),
        (26, '26-50'),
        (51, '51-70'),
        (71, '71-120'),
    ]

    EVENT_TYPES = [
        ('birthday', 'День рождения'),
        ('anniversary', 'Юбилей'),
        ('wedding', 'Свадьба'),
        ('new_year', 'Новый год'),
        ('women_day', '8 марта'),
        ('other', 'Другое'),
    ]

    RELATIONSHIPS = [
        ('mother', 'Мама'),
        ('father', 'Папа'),
        ('wife', 'Жена'),
        ('husband', 'Муж'),
        ('son', 'Сын'),
        ('daughter', 'Дочь'),
        ('brother', 'Брат'),
        ('sister', 'Сестра'),
        ('grandmother', 'Бабушка'),
        ('grandfather', 'Дедушка'),
        ('friend', 'Друг'),
        ('colleague', 'Коллега'),
        ('teacher', 'Учитель'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    age_range = models.CharField(max_length=20, choices=AGE_RANGE_CHOICES, blank=True, null=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, blank=True, null=True)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIPS, blank=True, null=True)

    class Meta:
        ordering = ['name']  # Сортировка по имени продукта

    def __str__(self):
        return f"{self.name} ({self.get_currency_display()})"
