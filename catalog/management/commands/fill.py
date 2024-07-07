import json
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import Group, Permission

from catalog.models import Category, Product


def create_moderators_group():
    # Создаем группу модераторов
    mod_group, created = Group.objects.get_or_create(name='Модераторы')
    if created:
        # Добавляем права доступа
        change_product_perm = Permission.objects.get(codename='change_product')
        delete_product_perm = Permission.objects.get(codename='delete_product')
        mod_group.permissions.add(change_product_perm, delete_product_perm)
        mod_group.save()
        print('Группа "Модераторы" успешно создана и настроена.')
    else:
        print('Группа "Модераторы" уже существует.')


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        categories = []
        # Здесь мы получаем данные из фикстуры с категориями
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "catalog.category":
                    categories.append(item)
        return categories

    @staticmethod
    def json_read_products():
        products = []
        # Здесь мы получаем данные из фикстуры с продуктами
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "catalog.product":
                    products.append(item['fields'])
        return products

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;")
            cursor.execute(f"TRUNCATE TABLE catalog_product RESTART IDENTITY CASCADE;")
        # Удалите все продукты
        Product.objects.all().delete()
        # Удалите все категории
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(Category(
                pk=category['pk'],
                category_name=category['fields']['category_name'],
                category_description=category['fields']['category_description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(Product(
                product_name=product['product_name'],

                product_description=product['product_description'],
                imagery=product['imagery'],
                category=Category.objects.get(pk=product['category']),
                cost_product=product['cost_product']))

        print(product_for_create)

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)


create_moderators_group()
