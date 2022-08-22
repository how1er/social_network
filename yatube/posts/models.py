from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from turtle import title
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ImageField

# Create your models here.

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField(max_length=500)
    pub_date = models.DateField("date published", auto_now_add = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="posts", blank=True, null = True)

    # поле для картинки 
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    def __str__(self):
       # выводим текст поста 
       return self.text

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=100)
    created = models.DateField('date created', auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')