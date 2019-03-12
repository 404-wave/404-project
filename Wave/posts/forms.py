
    
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "content",
            "image",
            "privacy",
            "accessible_users",
            "unlisted"
        ]


    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['privacy'].widget.attrs['class'] = "custom-select"
        #self.set_form_class()

        

            #add class for css
    def set_form_class(self):
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "custom-select"
        