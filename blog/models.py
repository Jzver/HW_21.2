from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """Класс для создания модели блоговой записи
    """

    title = models.CharField(max_length=150, verbose_name='Заголовок', help_text='Введите название статьи')
    slug = models.CharField(max_length=150, verbose_name='slug')
    content = models.TextField(verbose_name='Содержимое', **NULLABLE, help_text='Добавьте содержимое')
    preview = models.ImageField(upload_to='blog_foto', verbose_name='Изображение', **NULLABLE,
                                help_text='Добавьте изображение')
    date_of_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    view_counter = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('date_of_creation', 'is_published',)

    def __str__(self):
        return self.title