from dataclasses import field, fields
from django.forms import ModelForm, Textarea
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text','group', 'image']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
       
        fields = ['text']