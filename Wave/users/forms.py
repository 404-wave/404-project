from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=User._meta.get_field("first_name").max_length, required=False)
    last_name = forms.CharField(max_length=User._meta.get_field("last_name").max_length, required=False)
    email = forms.CharField(max_length=User._meta.get_field("email").max_length)
    github = forms.CharField(max_length=User._meta.get_field("github").max_length, required=False)
    bio = forms.CharField(max_length=User._meta.get_field("bio").max_length,  required=False)
    class Meta(UserCreationForm):
        model = User
        fields = ("username", "first_name", "last_name", "email", "github")
