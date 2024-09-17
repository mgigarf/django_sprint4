from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from blog.constants import NUMBER_OF_POSTS_ON_PAGE
from blog.models import Comment, Post


def get_posts_query_set(owner=None):
    if owner:
        kwargs = {'author': owner}
    else:
        kwargs = {'is_published': True, 'category__is_published': True,
                  'pub_date__lte': timezone.now()}
    return (Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(**kwargs).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date'))


def get_paginator(request, posts):
    page_number = request.GET.get('page')
    paginator = Paginator(posts, NUMBER_OF_POSTS_ON_PAGE)
    return paginator.get_page(page_number)


def authorize(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('comment_id'):
            instance = get_object_or_404(Comment, id=kwargs.get('comment_id'))
            if not args[0].user.id == instance.author_id:
                return redirect(
                    'blog:post_detail', post_id=kwargs.get('post_id')
                )
        elif kwargs.get('post_id'):
            instance = get_object_or_404(Post, id=kwargs.get('post_id'))
            if not args[0].user.id == instance.author_id:
                return redirect(
                    'blog:post_detail', post_id=kwargs.get('post_id')
                )
        return func(*args, **kwargs)
    return wrapper
