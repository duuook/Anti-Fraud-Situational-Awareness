from django import template

register = template.Library()

@register.filter
def to_percentage(value):
    return '{:.2%}'.format(value)