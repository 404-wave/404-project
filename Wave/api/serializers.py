from rest_framework import serializers
from core.models import Post, Comment
from users.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'bio', 'github')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user_id', 'content', 'date', 'privacy')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user_id', 'content', 'date')


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
