from .models import Category, Article
from modeltranslation.translator import TranslationOptions, register


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
    )

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = {
        "title",
        "short_description",
        "full_description"
    }