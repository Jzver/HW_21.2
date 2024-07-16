from config.settings import CASHES_ENABLED
from django.core.cache import cache
from catalog.models import Category, Product


def get_categories():
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories, 60 * 15)  # Кеширование на 15 минут
    return categories


def get_products():
    products = cache.get('products')
    if not products:
        products = Product.objects.all()
        cache.set('products', products, 60 * 15)  # Кеширование на 15 минут
    return products
