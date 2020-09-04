from django import template

register = template.Library()

@register.filter('times')
def times(x):

    return list(range(x))
