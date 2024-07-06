from django.contrib import admin
from catalog.models import Category, Product, Version
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


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
class VersionAdmin(admin.ModelAdmin):  # Изменено имя класса
    """ Класс для регистрации версии в админке."""
    list_display = ('id', 'product', 'name', 'number', 'is_current')
    list_filter = ('product',)
    search_fields = ('name',)


@admin.register(User)  # Исправлено на стандартную модель пользователя
class UserAdmin(admin.ModelAdmin):  # Изменено имя класса
    list_display = ('id', 'email', 'phone', 'country', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'country')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'avatar')}),
        ('Personal info', {'fields': ('phone', 'country')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone', 'country', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'phone', 'country')
    ordering = ('email',)
