from django import template

register = template.Library()


@register.filter(name='get_author_name')
def get_author_name(value1):
    if (value1.id):
        print (type(value1))
        print ("HERE", value1.id)
