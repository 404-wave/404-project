from django import forms

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(label="", widget=forms.Textarea)
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)