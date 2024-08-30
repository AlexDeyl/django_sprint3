from django.http import HttpRequest, HttpResponse, Http404
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category


utc_now = datetime.now(timezone.utc)


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница"""
    template = "blog/index.html"
    now = timezone.now()
    # Выводим на главную стрницу 5 последих постов
    post_list = Post.objects.filter(
        pub_date__lte=now, is_published=True, category__is_published=True
    ).order_by("-pub_date")[:5]
    context = {"post_list": post_list}
    return render(request, template, context)


def post_detail(request: HttpRequest, pk) -> HttpResponse:
    """Детали поста"""
    template = "blog/detail.html"
    post = get_object_or_404(Post, pk=pk, is_published=True)
    if post.pub_date > timezone.now() or not post.is_published:
        raise Http404("Пост не опубликован или устарел")
    if not post.category.is_published:
        raise Http404("Категория снята с публикации")
    context = {"post": post}
    return render(request, template, context)


def category_posts(request: HttpRequest, category_slug) -> HttpResponse:
    """Страница по категориям"""
    template = "blog/category.html"
    try:
        category = Category.objects.get(slug=category_slug, is_published=True)
    except Category.DoesNotExist:
        raise Http404("Категория не существует")
    # Получаем все посты, связанные с данной категорией
    posts = category.post_set.all()
    # Фильтруем посты, чтобы отображать только опубликованные
    post_list = list(
        filter(
            lambda post:
                post.is_published and not post.pub_date > timezone.now(), posts
        )
    )
    context = {"category": category, "post_list": post_list}
    return render(request, template, context)
