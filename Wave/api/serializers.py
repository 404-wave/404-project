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
