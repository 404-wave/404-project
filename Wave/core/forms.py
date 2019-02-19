from django import forms
from django.contrib.auth.forms import UserChangeForm
from users.models import User

class ProfileChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ('first_name','last_name','bio','github')
