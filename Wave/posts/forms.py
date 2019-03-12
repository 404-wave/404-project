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
            "unlisted",
            "user",
            "publish"
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['publish'].widget = forms.HiddenInput()

    def save(self, commit=True):
        accessible_users = self.cleaned_data.pop('accessible_users', [])
        print(accessible_users)
        post = super().save(commit)
        post.save()
        post.accessible_users.add(*accessible_users)
        post.accessible_users.add(post.user)
        return post
