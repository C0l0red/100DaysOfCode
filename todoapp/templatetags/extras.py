from django import template

register = template.Library()

@register.filter(name='color')
def color(num):
    num = len(num)
    if not num:
        return "danger"
    if 1 <= num <= 5:
        return "warning"
    if 5 < num <= 15:
        return "primary"
    else:
        return "success"