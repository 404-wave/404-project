from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=User._meta.get_field("first_name").max_length)
    last_name = forms.CharField(max_length=User._meta.get_field("last_name").max_length)
    github = forms.CharField(max_length=User._meta.get_field("github").max_length)
    bio = forms.CharField(max_length=User._meta.get_field("bio").max_length)

    class Meta(UserCreationForm):
        model = User
        fields = ("username", "first_name", "last_name", "github", "bio")
