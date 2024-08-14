from django import template
from datetime import datetime


register = template.Library()

@register.filter
def get_id(value):
    return str(value.get('_id'))

@register.filter
def to(value, arg):
    return range(value, arg + 1)


@register.filter
def format_date(value, date_format='%Y-%m-%d'):
    if isinstance(value, str):
        try:
            date_obj = datetime.strptime(value, '%Y-%m-%d')
            return date_obj.strftime(date_format)
        except ValueError:
            return value
    return value
