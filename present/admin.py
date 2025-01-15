from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "in_stock", 'currency')
    list_filter = ('currency', 'in_stock', 'category')
    search_fields = ('name', 'category__name')
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

