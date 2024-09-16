from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from blog.constants import NUMBER_OF_POSTS_ON_PAGE
from blog.models import Category, Post, Comment
from blog.forms import PostForm, CommentForm, UserForm

def get_posts_query_set():
    return (
        (Post.objects
         .select_related('category', 'location', 'author')
         .filter(
            is_published=True, category__is_published=True,
            pub_date__lte=timezone.now())
        ).annotate(comment_count=Count('blog_comments')).order_by('-pub_date'))


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


def index(request):
    posts = get_posts_query_set()
    page_obj = get_paginator(request, posts)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.author == request.user:
        post = get_object_or_404(get_posts_query_set(), id=post_id)
    comment = post.blog_comments.select_related('author')
    form = CommentForm()
    return render(
        request, 'blog/detail.html',
        {'post': post, 'comments': comment, 'form': form}
    )


def category_posts(request, category):
    category = get_object_or_404(Category, slug=category, is_published=True)
    post_list = get_posts_query_set().filter(category=category)
    page_obj = get_paginator(request, post_list)
    return render(request, 'blog/category.html',
                  {'category': category, 'page_obj': page_obj})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None,)
    context = {'form': form}
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', context)


@authorize
def edit_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', context)


@authorize
def delete_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, id=post_id)
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@authorize
def edit_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', context)


@authorize
def delete_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, id=comment_id)
    context = {'comment': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', context)


def profile_info(request, username):
    profile = get_object_or_404(User, username=username)
    if not profile == request.user:
        posts = get_posts_query_set().filter(author=profile)
    else:
        posts = (
            Post.objects.select_related('author', 'category', 'location')
            .filter(author=profile)
            .annotate(comment_count=Count('blog_comments'))
            .order_by('-pub_date'))
    page_obj = get_paginator(request, posts)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})
