from rest_framework import serializers
from posts.models import Post
from comments.models import Comment
from users.models import User

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

    # title - probably won't include
    # soure - more relevant for part 2
    # origin - more relevant for part 2
    # description - probably won't include
    # catgeories - probably won't include

    contentType = serializers.SerializerMethodField('_content_type')
    author = serializers.SerializerMethodField('_author')
    comments = serializers.SerializerMethodField('_comments')
    published = serializers.SerializerMethodField('_published')
    visibility = serializers.SerializerMethodField('_visibility')
    visible_to = serializers.SerializerMethodField('_visible_to')

    class Meta:
        model = Post
        fields = ('id', 'user', 'contentType', 'published', 'author', 'comments', 'visibility', 'visible_to', 'unlisted')

    def _content_type(self, obj):
        return obj.content_type

    def _published(self, obj):
        return obj.publish

    def _visibility(self, obj):
        return Post.Privacy[obj.privacy][1]

    def _visible_to(self, obj):
        if obj.privacy is Post.PUBLIC:
            return list()

        # TODO: Return a list of users who can view the post...
        # How to use the accessible_users list?
        user_list = list()
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
        fields = ('author', 'comment', 'contentType', 'published', 'id')

    def _author(self, obj):
        author = User.objects.get(username=obj.user)
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


# class FriendSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Friend
#         fields = ()
#         http_method_names = ['post']
#
#
# class FriendToFriendSerializer(serializers.ModelSerializer):
#
#     class MEta:
#         model = Friend
#         fields = ()
#         http_method_names ['get']
