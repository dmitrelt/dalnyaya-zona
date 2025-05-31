from django import template
from ..models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.filter
def truncate_chars(value, max_length):
    if len(value) <= max_length:
        return value
    return value[:max_length] + "..."
