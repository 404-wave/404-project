from rest_framework import serializers

from comments.models import Comment
from users.models import User, Node, NodeSetting
from posts.models import Post

import requests
from requests.auth import HTTPBasicAuth


class UserSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField('_id')
    friends = serializers.SerializerMethodField('_friends')
    displayName = serializers.SerializerMethodField('_username')
    firstName = serializers.SerializerMethodField('_first_name')
    lastName = serializers.SerializerMethodField('_last_name')

    class Meta:
        model = User

        fields = ('id', 'host', 'displayName', 'url', 'friends', 'github',
                    'firstName', 'lastName', 'email', 'bio')

    def _id(self, obj):
        request = self.context.get('request')
        host = request.scheme + "://" + request.META['HTTP_HOST']
        return host + "/author/" + str(obj.id)

    def _friends(self, obj):

        friends = list()
        friends_list = self.context.get('friends')
        print("Here is the friends list...")
        print(friends_list)
        for friend in friends:
            print(friend)
            try:
                friends.append(User.objects.get(id=friend))
            except:
                print("Didn't find it in our db, trying foreign servers...")
                for node in Node.objects.all():
                    url = node.host + "/author/" + str(friend) + "/"
                    r = requests.get(url, auth=HTTPBasicAuth(node.username, node.password))
                    if (r.status_code == 200):
                        try:
                            json = r.json()
                            username = json['displayName']
                            github = json['github']
                            host = json['host']
                            url = json['url']
                            id = json['id']
                            friends.append(User(host=host, id=id, github=github, url=url, username=username))
                            break
                        except Exception as e:
                            print("When attempting to serialize a foreign friend, the following exception occurred...")
                            print(e)
                            pass
                    else:
                        continue

        serialized_friends = UserFriendSerializer(friends, many=True,
            context={'request': self.context.get('request')})
        print("Here is the serialized result of the friends list...")
        print(serialized_friends.data)
        return serialized_friends.data

    def _username(self, obj):
        return obj.username

    def _first_name(self, obj):
        return obj.first_name

    def _last_name(self, obj):
        return obj.last_name


# TODO: How does this work with FRIENDS on different servers????????//
class UserFriendSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField('_id')
    displayName = serializers.SerializerMethodField('_username')

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url')

    def _id(self, obj):
        try:
            host = request.scheme + "://" + self.context.get('request').META['HTTP_HOST']
            return host + "/author/" + str(obj.id)
        except:
            return str(obj.id)

    def _username(self, obj):
        return obj.username


class PostSerializer(serializers.ModelSerializer):

    source = serializers.SerializerMethodField('_source')
    origin = serializers.SerializerMethodField('_origin')
    author = serializers.SerializerMethodField('_author')
    comments = serializers.SerializerMethodField('_comments')
    published = serializers.SerializerMethodField('_published')
    visibility = serializers.SerializerMethodField('_visibility')
    visibleTo = serializers.SerializerMethodField('_visible_to')
    categories = serializers.SerializerMethodField('_categories')
    description = serializers.SerializerMethodField('_description')
    title = serializers.SerializerMethodField('_title')
    source = serializers.SerializerMethodField('_source')
    origin = serializers.SerializerMethodField('_origin')

    contentType = serializers.SerializerMethodField('_content_type')

    class Meta:
        model = Post
        fields = ('id', 'user', 'contentType', 'categories', 'description',
                  'published', 'title', 'content', 'author', 'comments', 'visibility',
                  'visibleTo', 'unlisted', 'source', 'origin')

    def _source(self, obj):
        try:
            node_settings = NodeSetting.objects.all()[0]
            url_to_post = node_settings.host + "/posts/" + str(obj.id) + "/"
            return url_to_post
        except:
            return ""

    def _origin(self, obj):
        posts = Post.objects.filter(id=obj.id)
        if posts is None:
            found = False
            for node in Node.objects.all():
                # TODO: This probably needs to be changed to handle
                # more servers other than just our 1 partner.
                headers = {'X-UUID': self.context.get('requestor')}
                url_to_node = node.host + '/posts/' + str(obj.id) + '/'
                r = requests.get(node.host, headers=headers, auth=HTTPBasicAuth(node.username, node.password))
                try:
                    r = response.json()
                    if r.status_code == 200:
                        origin = r['posts'][0]['source']
                        return origin
                except:
                    pass

            if not found:
                return ''

        else:
            return self._source(obj)


    def _categories(self, obj):
        return list()

    def _description(self, obj):
        if obj.is_image:
            return "Image post"
        return "Text post"

    def _title(self, obj):
        return str(obj.title)

    def _content_type(self, obj):
        return obj.content_type

    def _published(self, obj):
        return obj.publish.isoformat()

    def _visibility(self, obj):
        return Post.Privacy[obj.privacy][1]

    def _visible_to(self, obj):
        user_list = list()
        if obj.privacy is Post.PRIVATE:
            return obj.accessible_users

    def _author(self, obj):
        # TODO: What if the author is from a different server??? FOAF!
        author = User.objects.get(username=obj.user)
        serialized_author = PostAuthorSerializer(author, many=False, context={'request':self.context.get('request')})
        return serialized_author.data

    def _comments(self, obj):
        post_id = obj.id
        comments = Post.objects.filter(id=post_id)[0].comments
        serialized_comments = CommentSerializer(comments, many=True, context={'request':self.context.get('request')})
        return serialized_comments.data


class PostAuthorSerializer(serializers.ModelSerializer):

    displayName = serializers.SerializerMethodField('_username')
    id = serializers.SerializerMethodField('_id')

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url', 'github')

    def _id(self, obj):
        request = self.context.get('request')
        host = request.scheme + "://" + request.META['HTTP_HOST']
        return host + "/author/" + str(obj.id)

    def _username(self, obj):
        return obj.username


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField('_author')
    published = serializers.SerializerMethodField('_published')
    comment = serializers.SerializerMethodField('_comment')

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'published', 'id')

    def _author(self, obj):

        try:
            author = User.objects.get(id=obj.user)
        except:
            found = False
            for node in Node.objects.all():
                url = node.host + "/author/" + str(obj.user) + "/"
                r = requests.get(url, auth=HTTPBasicAuth(node.username, node.password))
                if (r.status_code == 200):
                    try:
                        json = r.json()
                        username = json['displayName']
                        github = json['github']
                        host = json['host']
                        url = json['url']
                        id = json['id']
                        author = User(host=host, id=id, github=github, url=url, username=username)
                        found = True
                        break
                    except:
                        # TODO: What to do when the host of the author sends bad data?
                        return dict()
                else:
                    continue
            if not found:
                # TODO: What to do when the author no longer exists? OR, when them
                # author does exist, but the server is not sharing with us anymore.
                return dict()

        serialized_author = CommentAuthorSerializer(author, many=False, context={'request':self.context.get('request')})
        return serialized_author.data

    def _published(self, obj):
        return obj.published

    def _comment(self, obj):
        return obj.content


class CommentAuthorSerializer(serializers.ModelSerializer):

    displayName = serializers.SerializerMethodField('_username')
    id = serializers.SerializerMethodField('_id')

    class Meta:
        model = User
        fields = ('id', 'url', 'host', 'displayName', 'github')

    def _username(self, obj):
        return obj.username

    def _id(self, obj):
        try:

            author = User.objects.get(id=obj.id)
            request = self.context.get('request')
            host = request.scheme + "://" + request.META['HTTP_HOST']
            return host + "/author/" + str(obj.id)

        except Exception as e:

            for node in Node.objects.all():
                url = node.host + "/author/" + str(obj.id) + "/"
                r = requests.get(url, auth=HTTPBasicAuth(node.username, node.password))
                if (r.status_code == 200):
                    try:
                        json = r.json()
                        return json['id']
                    except:
                        print("When serializing the foreign author of a comment, the following exception occured...")
                        print(e)
                        pass
                else:
                    continue

            return str(obj.id)
