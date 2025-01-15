from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('RUB', 'Russian Ruble (₽)'),
    ]

    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    def __str__(self):
        return f"{self.name} ({self.get_currency_display()})"
