from django import template
from users.models import User
import re

register = template.Library()


@register.filter(name='get_author_name')
def get_author_name(value1):
    if (isinstance(value1, dict)):
        return (value1['author']['displayName'])
    else:
        return value1.user


@register.filter(name='get_post_type')
def get_post_type(value1):
    if (isinstance(value1, str)):
        return False
    else:
        return True


@register.filter(name='get_author_id')
def get_author_id(value1):
    if (isinstance(value1, dict)):
        id = value1['author']['id']
        id_regex = '(.*)([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$)'
        re_result = re.search(id_regex, id)
        id = re_result.group(2)
        host = value1['author']['host']
        host = re.sub('^https?:\/\/', '', host)
        host = re.sub('\/', '', host)
        return (host+id)
    else:
        id = User.objects.filter(username=value1.user)[0].id
        return id


@register.filter(name='get_privacy')
def get_privacy(value1):
    if (isinstance(value1, dict)):
        return (value1['visibility'])
    if (isinstance(value1, str)):
        return
    else:
        return value1.get_privacy_display()


@register.filter(name='get_comment_author')
def get_comment_author(value1):
    # print(value1)
    try:
        if (isinstance(value1, dict)):
            return (value1['author']['displayName'])
        else:
            return value1.user
    except:
        return 'foreign user'


@register.filter(name='get_comment_content')
def get_comment_content(value1):
    # print(value1)
    if (isinstance(value1, dict)):
        return (value1['comment'])
    else:
        return value1.content
