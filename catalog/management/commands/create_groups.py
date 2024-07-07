from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группы пользователей'

    def handle(self, *args, **options):
        self.create_moderators_group()

    def create_moderators_group(self):
        # Создаем группу модераторов
        mod_group, created = Group.objects.get_or_create(name='Модераторы')
        if created:
            # Добавляем права доступа
            change_product_perm = Permission.objects.get(codename='change_product')
            delete_product_perm = Permission.objects.get(codename='delete_product')
            mod_group.permissions.add(change_product_perm, delete_product_perm)
            mod_group.save()
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" успешно создана и настроена.'))
        else:
            self.stdout.write('Группа "Модераторы" уже существует.')
