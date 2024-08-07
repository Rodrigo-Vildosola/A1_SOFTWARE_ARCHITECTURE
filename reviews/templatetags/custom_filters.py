from django import template

register = template.Library()

@register.filter
def get_id(value):
    return str(value.get('_id'))
