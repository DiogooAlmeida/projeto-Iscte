from django import template

register = template.Library()

@register.filter
def split(value, key):
    """
    Returns the value turned into a list after splitting it by key.
    """
    return value.split(key)