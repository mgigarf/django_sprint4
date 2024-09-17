from django.contrib.auth import get_user_model
from django.db import models

from blog.constants import TITLE_MAX_LENGTH, PREVIEW_LIMIT

User = get_user_model()


class PublishedCreatedModel(models.Model):
    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_created=True, verbose_name='Добавлено', auto_now_add=True
    )

    class Meta:
        abstract = True


class Location(PublishedCreatedModel):
    name = models.CharField(
        max_length=TITLE_MAX_LENGTH, verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:PREVIEW_LIMIT]


class Category(PublishedCreatedModel):
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True, verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:PREVIEW_LIMIT]


class Post(PublishedCreatedModel):
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH, verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True,
        verbose_name='Местоположение', blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(null=True, upload_to='post_image', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', )
        default_related_name = 'posts'

    def __str__(self):
        return self.title[:PREVIEW_LIMIT]


class Comment(PublishedCreatedModel):

    text = models.TextField(verbose_name='Текст')

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор комментария'
    )

    created_at = models.DateTimeField(
        auto_created=True, verbose_name='Добавлено', auto_now_add=True
    )

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Автор комментария'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at', )
        default_related_name = 'comments'

    def __str__(self):
        result_string = (f'Комментарий пользователя {self.author.username} '
                         f'для поста {self.post.title[:PREVIEW_LIMIT]}')
        return result_string
