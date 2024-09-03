from django.db import models

from django.contrib.auth.models import User

from django.conf import settings

from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=settings.CONSTANTS['MAX_LENGTH'],
                             blank=False,
                             verbose_name='Заголовок')
    text = models.TextField(blank=False,
                            verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.')
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
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    @classmethod
    def get_recent_posts(cls):
        return cls.objects.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=settings.CONSTANTS['MAX_LENGTH'],
                             blank=False,
                             verbose_name='Заголовок')
    description = models.TextField(blank=False,
                                   verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(max_length=settings.CONSTANTS['MAX_LENGTH'],
                            blank=False,
                            verbose_name='Название места')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
