from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.models import Post, Category


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница"""
    template = "blog/index.html"
    post_list = Post.get_recent_posts()
    context = {"post_list": post_list}
    return render(request, template, context)


def post_detail(request: HttpRequest, post_id) -> HttpResponse:
    """Детали поста"""
    template = "blog/detail.html"
    post = get_object_or_404(Post, pk=post_id, is_published=True)
    if post.pub_date > timezone.now() or not post.is_published:
        raise Http404("Пост не опубликован или устарел")
    if not post.category.is_published:
        raise Http404("Категория снята с публикации")
    context = {"post": post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """Страница по категориям"""
    template = "blog/category.html"
    try:
        category = Category.objects.get(slug=category_slug, is_published=True)
    except Category.DoesNotExist:
        raise Http404("Категория не существует")
    published_posts = Post.objects.filter(category=category,
                                          is_published=True,
                                          pub_date__lte=timezone.now())
    context = {'category': category, 'post_list': published_posts}
    return render(request, template, context)
