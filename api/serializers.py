from rest_framework import serializers
from posts.models import Post
from comments.models import Comment
from users.models import User, Node

import requests

class UserSerializer(serializers.ModelSerializer):

    friends = serializers.SerializerMethodField('_friends')
    displayName = serializers.SerializerMethodField('_username')
    firstName = serializers.SerializerMethodField('_first_name')
    lastName = serializers.SerializerMethodField('_last_name')

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url', 'friends', 'github', 'firstName', 'lastName', 'email', 'bio')

    def _friends(self, obj):
        friends = self.context.get('friends')
        serialized_friends = UserFriendSerializer(friends, many=True)
        return serialized_friends.data

    def _username(self, obj):
        return obj.username

    def _first_name(self, obj):
        return obj.first_name

    def _last_name(self, obj):
        return obj.last_name


class UserFriendSerializer(serializers.ModelSerializer):

    displayName = serializers.SerializerMethodField('_username')

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url')

    def _username(self, obj):
        return obj.username


class PostSerializer(serializers.ModelSerializer):

    contentType = serializers.SerializerMethodField('_content_type')
    author = serializers.SerializerMethodField('_author')
    comments = serializers.SerializerMethodField('_comments')
    published = serializers.SerializerMethodField('_published')
    visibility = serializers.SerializerMethodField('_visibility')
    visible_to = serializers.SerializerMethodField('_visible_to')
    categories = serializers.SerializerMethodField('_categories')
    description = serializers.SerializerMethodField('_description')
    source = serializers.SerializerMethodField('_source')
    origin = serializers.SerializerMethodField('_origin')


    class Meta:
        model = Post
        fields = ('id', 'user', 'contentType', 'categories', 'description',
                    'published', 'content', 'author', 'comments', 'visibility',
                     'visible_to', 'unlisted', 'source', 'origin')

    # TODO
    def _source(self, obj):
        return ""

    # TODO:
    def _origin(self, obj):
        return ""

    def _categories(self, obj):
        return list()

    def _description(self, obj):
        return ""

    def _content_type(self, obj):
        return obj.content_type

    def _published(self, obj):
        return obj.publish

    def _visibility(self, obj):
        return Post.Privacy[obj.privacy][1]

    def _visible_to(self, obj):
        user_list = list()
        if obj.privacy is Post.PRIVATE:
            for user in obj.accessible_users.all():
                user_list.append(str(user.id))
        return user_list

    def _author(self, obj):
        author = User.objects.get(username=obj.user)
        serialized_author = PostAuthorSerializer(author, many=False)
        return serialized_author.data

    def _comments(self, obj):
        post_id = obj.id
        comments = Post.objects.filter(id=post_id)[0].comments
        serialized_comments = CommentSerializer(comments, many=True)
        return serialized_comments.data


class PostAuthorSerializer(serializers.ModelSerializer):

    displayName = serializers.SerializerMethodField('_username')
    id = serializers.SerializerMethodField('_id')

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url', 'github')

    def _username(self, obj):
        return obj.username

    def _id(self, obj):
        return str(obj.host) + str(obj.id)


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
                url = node.host + "/service/author/" + str(obj.user)
                r = requests.get(url)
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
                    except:
                        # TODO: What to do when the host of the author sends bad data?
                        return dict()
                else:
                    continue
            if not found:
                # TODO: What to do when the author no longer exists? OR, when them
                # author does exist, but the server is not sharing with us anymore.
                return dict()

        serialized_author = CommentAuthorSerializer(author, many=False)
        return serialized_author.data

    def _published(self, obj):
        return obj.timestamp

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
        return str(obj.host) + str(obj.id)
