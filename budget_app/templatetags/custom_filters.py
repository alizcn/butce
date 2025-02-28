from django import template
from decimal import Decimal
from builtins import sum as builtins_sum

register = template.Library()

@register.filter
def div(value, arg):
    """Divides the value by the argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    """Multiply the value by the argument"""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def sum(value, key):
    """Sum a list of dictionaries by key"""
    try:
        return builtins_sum(Decimal(str(item[key])) for item in value)
    except (ValueError, TypeError, KeyError):
        return 0

@register.filter
def add_class(field, css_class):
    """Add a CSS class to a form field"""
    return field.as_widget(attrs={"class": css_class}) 