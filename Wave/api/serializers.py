from rest_framework import serializers
from posts.models import Post
from comments.models import Comment
from users.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'bio', 'github')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('user', 'content', 'publish', 'privacy')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user', 'content', 'date')


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
