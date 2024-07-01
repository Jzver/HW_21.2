from django.contrib import admin
from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс для регистрации категории в админке."""
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Класс для регистрации продукта в админке."""
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Version)
class ProductAdmin(admin.ModelAdmin):
    """ Класс для регистрации версии в админке."""
    list_display = ('id', 'product', 'name', 'number', 'is_current')
    list_filter = ('product',)
    search_fields = ('name',)