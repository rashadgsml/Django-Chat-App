from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'id': 'description'}))
    class Meta:
        model = Post
        fields = ["image","description"]
