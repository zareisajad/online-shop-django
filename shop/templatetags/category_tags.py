from django import template

register = template.Library()

@register.inclusion_tag('category_tree.html')
def draw_category_tree(categories):
    return {'categories': categories}


@register.simple_tag
def get_category_ancestors(category):
    ancestors = []
    while category:
        ancestors.append(category)
        category = category.sub_category
    return list(reversed(ancestors))