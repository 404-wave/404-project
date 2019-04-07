from django import forms

from mimetypes import guess_type
import base64
import os

from .models import Post 
from users.models import User
from friends.models import FollowManager
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "content",
            "image",
            "privacy",
            "content_type",
            "accessible_users",
            "unlisted",
            "user",
            "publish"
        ]
        widgets = {'accessible_users': forms.CheckboxSelectMultiple} 
    
    def __init__(self, *args, **kwargs):
        print ("FORMSFORMS")
        print ("FORMS", args, kwargs)
        user_details = kwargs.pop('user_details', None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['publish'].widget = forms.HiddenInput()
        self.choices(user_details)
        self.fields['accessible_users'] = forms.MultipleChoiceField(
                label="question",
                required=False,
                widget=forms.CheckboxSelectMultiple,
                choices=self.choices(user_details)
                ) 

        self.set_placeholder('content', 'What\'s on your mind?')
        self.set_form_class()

    def choices(self, user_id):
        print ("USER choice")
        users = User.objects.all()
        options = []
        for user in users:
            options.append((user.host+'/'+str(user.id),user.username))
        followManager = FollowManager()
        friends = followManager.get_friends(user_id)
        return options

    #add placeholder text to fields
    def set_placeholder(self, field, text):
        self.fields[field].widget.attrs['placeholder'] = text

    #add class for css
    def set_form_class(self):
            self.fields['content'].widget.attrs['class'] = "create_post"
            self.fields['unlisted'].widget.attrs['class'] = "create_post"

    """
        Creates the objects for the accessible useres and then save to the form
    """
    def save(self, commit=True):

        #accessible_users = self.cleaned_data
     
        post = super().save(commit)
        username = post.user.username
        timestamp = post.timestamp.strftime("%b %-d, %Y, at %H:%M %p")
        post.title = username+" - "+timestamp
        post.save()
        print
        #post.accessible_users.add(*accessible_users)
        #post.accessible_users.add(post.user)
        return post


class ImageForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "image",
            "privacy",
            "accessible_users",
            "user",
            "publish"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['publish'].widget = forms.HiddenInput()

    """
        Creates the objects for the accessible useres and then save to the form
    """
    def save(self, commit=True):
        #accessible_users = self.cleaned_data.pop('accessible_users', [])
        print("KK")
        post = super().save(commit)
        username = post.user.username
        timestamp = post.timestamp.strftime("%b %-d, %Y, at %H:%M %p")
        post.title = username+" - "+timestamp
        post.save()
        #post.accessible_users.add(*accessible_users)
        #post.accessible_users.add(post.user)
        return post
