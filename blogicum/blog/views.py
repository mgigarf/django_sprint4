from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import CommentForm, PostForm, UserForm
from blog.models import Category, Comment, Post
from blog.service import authorize, get_paginator, get_posts_query_set


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
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
@authorize
def edit_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
@authorize
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {'form': form}
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


@login_required
@authorize
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
@authorize
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    context = {'comment': comment}
    return render(request, 'blog/comment.html', context)


def profile_info(request, username):
    profile = get_object_or_404(User, username=username)
    if not profile == request.user:
        posts = get_posts_query_set().filter(author=profile)
    else:
        posts = get_posts_query_set(owner=profile)
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
