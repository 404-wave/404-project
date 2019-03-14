
    
from django import forms

from .models import Post

import base64
import os
from mimetypes import guess_type


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "content",
            "image",
            "privacy",
            "accessible_users",
            "unlisted",
            "user",
            "publish"
        ]


    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.set_placeholder('content', 'What\'s on your mind?')
        self.set_form_class()
        print(self.fields['user'])


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
        accessible_users = self.cleaned_data.pop('accessible_users', [])
        print(accessible_users)
        post = super().save(commit)
        post.save()
        post.accessible_users.add(*accessible_users)
        post.accessible_users.add(post.user)
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
        accessible_users = self.cleaned_data.pop('accessible_users', [])
        print(accessible_users)
        post = super().save(commit)
        post.save()
        post.accessible_users.add(*accessible_users)
        post.accessible_users.add(post.user)
        return post

        

