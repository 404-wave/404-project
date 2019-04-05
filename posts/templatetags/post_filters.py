from django import template
from users.models import User
from posts.models import Post
import re
from datetime import datetime

register = template.Library()


@register.filter(name='get_author_name')
def get_author_name(value1):
    if (isinstance(value1, dict)):
        return (value1['author']['displayName'])+ ' from '+value1['author']['host']
    else:
        return value1.user


@register.filter(name='get_post_type')
def get_post_type(value1):
    if (isinstance(value1, str)):
        return False
    else:
        return True

@register.filter(name='get_time')
def get_time(value1):
    if (isinstance(value1, dict)):
        time =  re.sub(r'.[0-9]{2}:[0-9]{2}$','',value1['published']) 
        time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')  
        return datetime.strftime(time, '%b %d %Y %I:%M%p')
    else:
        return value1.timestamp




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

@register.filter(name='get_user')
def get_user(value, args):
    if (value['author']['id'] == str(args)):
        return True
    else:
        return False


@register.filter(name='get_comment_content')
def get_comment_content(value1):
    if (isinstance(value1, dict)):
        return (value1['comment'])
    else:
        return value1.content


@register.filter(name="get_edit")
def get_edit(value):
    post = Post()
    user = User()
    user.id = value['author']['id']
    post.id = value['id']
    post.user = user
    return post.get_edit_absolute_url()

@register.filter(name="get_delete")
def get_delete(value):
    post = Post()
    user = User()
    user.id = value['author']['id']
    post.id = value['id']
    post.user = user
    return post.get_delete_absolute_url()


@register.filter(name="markdown")
def markdown(value):
    content = 'bob'
    if (isinstance(value, dict)):
        print (value)
        content  = value['contentType']
    else:
        content = value.content_type
    if ("markdown" in content):
           return True
    return False


@register.filter(name='is_image_post')
def is_image_post(value1):
    if (isinstance(value1, dict)):
        if (value1['contentType'] == "image/jpeg;base64") or (value1['contentType'] == "image/png;base64"):
            return True
        else:
            return False
    else:
        if (value1.content_type == "image/jpeg;base64") or (value1.content_type == "image/png;base64"):
            return True
        else:
            return False
