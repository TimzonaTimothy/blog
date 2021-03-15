from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now 
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ckeditor.fields  import RichTextField
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='posts')
    title = models.CharField(max_length=250)
    image = models.FileField(upload_to='images/', blank=True)
    text = RichTextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=255, default='news')
    # likes = models.ManyToManyField('auth.User', related_name='blog_posts')

    def publish(self):
        self.published_date = now()
        self.save()


    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title + '|' + str(self.author)

    class Meta:
        ordering = ["-pk"]


class Comment(models.Model):
    post = models.ForeignKey('main.Post',related_name='comments', on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=250,blank=False,null=True)
    text = models.CharField(max_length=1000,blank=False)
    created_date = models.DateTimeField(auto_now_add=True)


    def get_absolute_url(self):
        return reverse('post_detail')

    def __str__(self):
        return self.text

class Subscribe(models.Model):
    email = models.EmailField(max_length=250,null=True)
    date_added = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=255)


    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.name