from django.conf import settings
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    slug = models.CharField(max_length=200, verbose_name='slug', **NULLABLE)
    preview = models.ImageField(upload_to='article_previews/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    view_count = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ('can_change_desc_permission', 'Can manage blog publications'),
        ]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
