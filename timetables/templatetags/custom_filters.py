from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    if value:
        return str(value).split(delimiter)
    return []