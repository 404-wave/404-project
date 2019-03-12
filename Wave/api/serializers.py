from rest_framework import serializers
from posts.models import Post
from comments.models import Comment
from users.models import User

class UserSerializer(serializers.ModelSerializer):

    friends = serializers.SerializerMethodField('_friends')
    displayName = serializers.SerializerMethodField('get_username')
    firstName = serializers.SerializerMethodField('get_first_name')
    lastName = serializers.SerializerMethodField('get_last_name')

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url', 'friends', 'github', 'firstName', 'lastName', 'email', 'bio')

    def _friends(self, obj):
        friends = self.context.get('friends')
        serialized_friends = UserFriendSerializer(friends, many=True)
        return serialized_friends.data

    # These need to be added to accomodate differences in naming convention
    # between our models and the example-article.json. The alternative is to
    # change the model attribute names and change the fields in the class Meta.
    def get_username(self, obj):
        return obj.username

    def get_first_name(self, obj):
        return obj.first_name

    def get_last_name(self, obj):
        return obj.last_name


class UserFriendSerializer(serializers.ModelSerializer):

    displayName = serializers.SerializerMethodField('get_username')

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName', 'url')

    def get_username(self, obj):
        return obj.username


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('user', 'content', 'publish', 'privacy')


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField('_author')
    published = serializers.SerializerMethodField('_published')
    comment = serializers.SerializerMethodField('_comment')

    # TODO: Change comment IDs to UUIDs
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

    displayName = serializers.SerializerMethodField('get_username')
    id = serializers.SerializerMethodField('build_id')

    class Meta:
        model = User
        fields = ('id', 'host', 'displayName')

    def get_username(self, obj):
        return obj.username

    def build_id(self, obj):
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
