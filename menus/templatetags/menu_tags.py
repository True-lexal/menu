from django import template
from django.http import Http404
from menus.utils import url_set
from menus.models import MenuElements

register = template.Library()


@register.inclusion_tag('menus/tags/menu_tag.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Draw menu named 'menu_name'
    """
    current_url = context['slug']
    menu = MenuElements.objects.filter(main_menu__name=menu_name).select_related('parent')
    menu_list = []
    tag_url_list = [x.url for x in menu]
    url_set.url_set = url_set.url_set.union(set(tag_url_list))
    if current_url and current_url in tag_url_list:

        current_link = next(filter(lambda x: x.url == current_url, menu))

        menu_list.append(current_link.pk)
        parent = current_link.parent
        while parent:
            menu_list.append(parent.pk)
            parent = next(filter(lambda x: x.pk == parent.pk, menu)).parent
        menu_list.append(None)

    return {'menu_list': menu_list, 'menu': menu, 'parent_pk': None, 'current_url': current_url}


@register.simple_tag(takes_context=True)
def check_urls(context):
    """
    Checks if exists url
    """
    current_url = context['slug']
    if current_url and current_url not in url_set.url_set:
        raise Http404
    url_set.url_set = set()
    return ''
