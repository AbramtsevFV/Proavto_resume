from django import template
from proauto.models import *

register = template.Library()

# основного меню
@register.inclusion_tag('proauto/menu.html')
def menu():
    return {'menu': Menu.objects.all()}