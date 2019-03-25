from django import template

register = template.Library()


@register.filter(name='get_author_name')
def get_author_name(value1):
    if (isinstance(value1, dict)): 
        print (type(value1))
    else:
        pass

