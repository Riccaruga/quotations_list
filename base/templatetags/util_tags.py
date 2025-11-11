# base/templatetags/util_tags.py

from django import template

register = template.Library()

@register.filter
def get_attribute(obj, name):
    """Dynamically gets an attribute from an object by string name."""
    return getattr(obj, name, None)

@register.filter
def get_attribute_display(obj, name):
    """
    Dynamically gets the display value for a field with choices
    using the get_FOO_display() method.
    """
    display_method = f'get_{name}_display'
    return getattr(obj, display_method, lambda: None)()