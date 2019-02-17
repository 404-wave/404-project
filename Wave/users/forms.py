from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=User._meta.get_field("first_name").max_length, required=False)
    last_name = forms.CharField(max_length=User._meta.get_field("last_name").max_length, required=False)
    email = forms.EmailField(max_length=User._meta.get_field("email").max_length)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Make sure it's more than 30 characters and includes a number and a lowercase letter."
        self.fields['password2'].help_text = "Enter the same password as above."
        self.fields['username'].help_text = None

    class Meta(UserCreationForm):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1")
        field_order = ["username", "first_name", "last_name", "email"]
