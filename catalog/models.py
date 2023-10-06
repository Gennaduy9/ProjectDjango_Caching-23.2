from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Изображение')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    color = models.CharField(max_length=50, **NULLABLE, verbose_name='Цвет')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, **NULLABLE, verbose_name='Категория')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.name} ({self.category}) - {self.price} руб.'

    class Meta:
        permissions = [
            ('can_change_is_published_permission', 'Can cancel product publication'),
            ('can_change_desc_permission', 'Can change product description'),
            ('can_change_category_permission', 'Can change product category'),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number_ver = models.CharField(max_length=50, **NULLABLE, verbose_name='Номер версии')
    name_ver = models.CharField(max_length=100, verbose_name='Название версии')
    activ_ver = models.BooleanField(default=False, verbose_name='Активная версия')

    def __str__(self):
        return self.name_ver

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


