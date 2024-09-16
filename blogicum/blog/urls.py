from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path(
        'posts/<int:post_id>/comment/', views.add_comment, name='add_comment'
    ),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('category/<slug:category>/', views.category_posts,
         name='category_posts'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_info, name='profile'),
    path('', views.index, name='index'),
]
