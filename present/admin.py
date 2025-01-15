from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "in_stock")
    search_fields = ("name", "category__name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

