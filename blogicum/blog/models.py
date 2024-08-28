from django.db import models
from django.contrib.auth.models import User


# Определяем модель Post
class Post(models.Model):
    title = models.CharField(max_length=256, blank=False,
                             verbose_name='Заголовок')
    text = models.TextField(blank=False, verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата  время публикации',
        help_text='''Если установить дату и время в будущем -
        можно деать отложены публкации''')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации')
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL, null=True,
        verbose_name='Местоположение')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL, null=True,
        verbose_name='Категория')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


# Определяем модель Category
class Category(models.Model):
    title = models.CharField(max_length=256, blank=False,
                             verbose_name='Заголовок')
    description = models.TextField(blank=False,
                                   verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='''Идентифкатор страицы для URL;
        разрешены символы латиницы, цифры, дефис, и подчеркиваие''')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


# Определяем модель Location
class Location(models.Model):
    name = models.CharField(max_length=256, blank=False,
                            verbose_name='Название места')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name
