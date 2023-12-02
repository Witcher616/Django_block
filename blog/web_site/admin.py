from django.contrib import admin

from .models import Category, Article, Favorite
from modeltranslation.admin import TranslationAdmin


class ArticleAdmin(TranslationAdmin):
    list_display = ('pk', 'title', 'created_at', 'views', 'category', 'author')
    list_display_links = ('pk', 'title')
    list_filter = ('created_at', 'category', 'author')
    list_editable = ('category', 'author')
    readonly_fields = ('views',)


class CategoryAdmin(TranslationAdmin):
    list_display = ('pk', 'name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Favorite)
admin.site.register(Article, ArticleAdmin)
