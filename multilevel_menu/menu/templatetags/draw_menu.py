from typing import Any, Dict, List

from django import template
from django.db.models.query import QuerySet

from menu.models import Item

register = template.Library()


@register.inclusion_tag('includes/menu.html', takes_context=True)
def draw_menu(context: Any, menu: str) -> Dict[str, Dict]:
    """Строим словарь, моделирующий меню."""
    # Слаг выбранного пункта меню
    item: str | None = context.request.resolver_match.kwargs.get('item', None)
    # Все пункты текущего меню
    all_menu: QuerySet = Item.objects.filter(
        menu__slug=menu).select_related('parent')
    # Если выбранный пункт в текущем меню, то получаем
    # его родительские и дочерние элементы
    if item_in_this_menu(all_menu, item):
        parents: List[Item | None] = get_parents(all_menu, item)
        childrens: Dict[Item, Dict[None, None]] = get_childrens(all_menu, item)
    # Если выбранный пункт не в текущем меню, то получаем только
    # пунткы верхнего уровня
    else:
        parents = childrens = {}
    temp = {}
    # Строим дерево от выбранного пункта до верхнего уровня
    for parent in parents:
        for element in all_menu:
            if element.parent == parent:
                temp[element] = childrens if element.slug == item else {}
        childrens = dict(temp)
        item = parent.slug
        temp = {}
    # Получаем пункты верхнего уровня
    for element in main(all_menu):
        temp[element] = childrens if element.slug == item else {}
    childrens = dict(temp)
    return {'items': childrens}


def get_parents(all_menu: QuerySet, item: str) -> List[Item | None]:
    """Получаем дерево родителей текущего пункта меню."""
    if not item:
        return []
    parents = []
    parent = 1
    while parent:
        for element in all_menu:
            if element.slug == item:
                if parent := element.parent:
                    parents.append(parent)
                    item = parent.slug
                break
    return parents


def get_childrens(all_menu: QuerySet, item: str | None
                  ) -> Dict[Item, Dict[None, None]]:
    """Получаем список детей текущего пункта меню."""
    return {
        element: {}
        for element in all_menu
        if (
            (item and element.parent and element.parent.slug == item)
            or (not item and not element.parent)
        )
    }


def main(all_menu: QuerySet) -> List[Item]:
    """Верхний уровень меню."""
    return [element for element in all_menu if not element.parent]


def item_in_this_menu(all_menu: QuerySet, item: str) -> bool:
    """Текущий пункт меню в этом меню?"""
    return any(element.slug == item for element in all_menu)
