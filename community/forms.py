from django import forms
from .models import Group, Post

class JoinGroupForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Select a Group")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
