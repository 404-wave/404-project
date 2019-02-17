from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=User._meta.get_field("first_name").max_length, required=False)
    last_name = forms.CharField(max_length=User._meta.get_field("last_name").max_length, required=False)
    email = forms.EmailField(max_length=User._meta.get_field("email").max_length)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        #customize help text
        self.set_help_text('password1', "Make sure it's more than 30 characters and includes a number and a lowercase letter.")
        self.set_help_text('password2', "Enter the same password as above.")
        self.set_help_text('username', None)
        #add in placeholder text to form input
        self.set_placeholder('email', 'your_email@address.com')
        self.set_placeholder('username', 'Your username')
        self.set_placeholder('first_name', 'Your first name')
        self.set_placeholder('last_name', 'Your last name')
        self.set_form_class()

    #customize help text associated with field
    def set_help_text(self, field, text):
        self.fields[field].help_text = text

    #add placeholder text to fields
    def set_placeholder(self, field, text):
        self.fields[field].widget.attrs['placeholder'] = text

    #add class for css
    def set_form_class(self):
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

    class Meta(UserCreationForm):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1")
        field_order = ["username", "first_name", "last_name", "email"]
