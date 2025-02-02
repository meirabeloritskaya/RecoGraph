from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)

    class Meta:
        ordering = ["name"]  # Сортировка по имени категории

    def __str__(self):
        return self.name


class Product(models.Model):
    CURRENCY_CHOICES = [
        ("RUB", "₽"),  # Russian Ruble
    ]

    GENDER_CHOICES = [
        ("male", "Мужчина"),
        ("female", "Женщина"),
    ]

    AGE_RANGE_CHOICES = [
        (0, "0-1"),
        (2, "2-6"),
        (7, "7-13"),
        (14, "14-25"),
        (26, "26-50"),
        (51, "51-70"),
        (71, "71-120"),
    ]

    # EVENT_TYPES = [
    #     ('birthday', 'День рождения'),
    #     ('anniversary', 'Юбилей'),
    #     ('wedding', 'Свадьба'),
    #     ('new_year', 'Новый год'),
    #     ('women_day', '8 марта'),
    #     ('other', 'Другое'),
    # ]
    #
    # RELATIONSHIPS = [
    #         ('mother', 'Мама/Папа'),
    #         ('wife', 'Жена/Муж'),
    #         ('daughter', 'Дочь/Сын'),
    #         ('sister', 'Сестра/Брат'),
    #         ('grandmother', 'Бабушка/Дедушка'),
    #         ('friend', 'Подруга/Друг'),
    #         ('other', 'Другое'),
    #     ]

    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    in_stock = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    price_range = models.CharField(max_length=25, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="RUB")
    gender = models.JSONField(
        default=list, blank=True
    )  # JSONField для хранения массивов
    age_range = models.JSONField(default=list, blank=True)
    # event_type = models.CharField(max_length=20, choices=EVENT_TYPES, blank=True, null=True)
    # relationship = models.CharField(max_length=20, choices=RELATIONSHIPS, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["name"]  # Сортировка по имени продукта

    def __str__(self):
        return f"{self.name} ({self.get_currency_display()})"
