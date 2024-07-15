from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True,
                             help_text='Введите номер телефона')
    country = models.CharField(max_length=50, verbose_name='Страна', blank=True, null=True, help_text='Введите страну')
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True, help_text='Загрузите свой аватар')
    token = models.CharField(max_length=64, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()  # Используем пользовательский менеджер

    def natural_key(self):
        return (self.email,)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email