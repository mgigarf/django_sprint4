from django.contrib import admin

from .models import Category, Location, Post

admin.site.register(Category)
admin.site.register(Location)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'pub_date',
        'category'
    )
    list_editable = (
        'is_published',
        'pub_date',
        'category'
    )

    search_fields = ('title',)
    list_filter = ('location',)
    list_display_links = ('title',)
    empty_value_display = 'Не задано'
    verbose_name = 'Публикацию'


admin.site.register(Post, PostAdmin)
