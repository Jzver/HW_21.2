from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    """Класс для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    """Класс для создание форм для модели Продукт"""
    banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name', 'description', 'preview', 'category', 'price')

    def clean_name(self):
        """Метод для проверки валидации имени Продукта при создании нового объекта"""
        cleaned_data = self.cleaned_data['name']
        if cleaned_data.lower() in self.banned_words:
            raise ValidationError(f'Слова, запрещенные к использованию в названии продукта: '
                                  f'{str(self.banned_words)[1:-2]}')
        return cleaned_data

    def clean_description(self):
        """Метод для проверки валидации описания Продукта при создании нового объекта"""
        cleaned_data = self.cleaned_data['description']
        if cleaned_data.lower() in self.banned_words:
            raise ValidationError(f'Слова, запрещенные к использованию в описании продукта: '
                                  f'{str(self.banned_words)[1:-2]}')
        return cleaned_data


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = ('id', 'product', 'name', 'number', 'is_current')
