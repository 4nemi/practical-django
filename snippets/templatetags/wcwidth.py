from djanngo.template import Library
from wcwidth import wcswidth as func_wcswidth


register = Library()

@register.filter(is_safe=False)
def wcswidth(value):
    if not isinstance(value, str):
        return 0
    return func_wcswidth(value)
