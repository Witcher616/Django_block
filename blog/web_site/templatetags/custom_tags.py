from django import template

from web_site.models import Category, Favorite


register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag()
def is_article_added_to_fav_by_user(user, article):
    if not user.is_authenticated:
        return False

    obj = Favorite.objects.filter(user=user, article=article).first()
    if obj is not None:
        return True
    return False


@register.simple_tag()
def count_user_favorites(user):
    return Favorite.objects.filter(user=user).count()
