from django import template

register = template.Library()


@register.simple_tag
def debe(debe , haber):
    value = 0
    if float(debe) > float(haber):
        value = 1
    return value


@register.simple_tag
def haber(debe, haber):
    value = 0
    if float(debe) < float(haber):
        value = 1
    return value


@register.simple_tag
def equals(debe, haber):
    value = 0
    if float(debe) == float(haber):
        value = 1
    return value
