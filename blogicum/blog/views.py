from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.constants import NUMBER_OF_POSTS_ON_MAIN_PAGE
from blog.models import Category, Post


def get_posts_query_set():
    return (Post.objects
            .select_related('category', 'location', 'author')
            .filter(
                is_published=True, category__is_published=True,
                pub_date__lte=timezone.now())
            )


def index(request):
    posts = get_posts_query_set()[:NUMBER_OF_POSTS_ON_MAIN_PAGE]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, post_id):
    post = get_object_or_404(get_posts_query_set(), id=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category):
    category = get_object_or_404(Category, slug=category, is_published=True)
    post_list = get_posts_query_set().filter(category=category)
    return render(request, 'blog/category.html',
                  {'category': category, 'post_list': post_list})
