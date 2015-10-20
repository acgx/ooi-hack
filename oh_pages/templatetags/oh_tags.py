from django import template
from django.utils.safestring import mark_safe
import lxml.html
from lxml.html.clean import Cleaner

register = template.Library()
cleaner = Cleaner()
cleaner.safe_attrs = lxml.html.defs.safe_attrs | {'style'}
cleaner.add_nofollow = True


@register.filter(name='xss_safe')
def xss_safe(value):
    return mark_safe(cleaner.clean_html(value))
