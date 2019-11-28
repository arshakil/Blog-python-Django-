from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from datetime import datetime 
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'    

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=5000)
    image = models.ImageField(upload_to='picture/%Y/%m/%d')
    description = models.TextField()
    post_uploaded = models.DateTimeField(default=datetime.now(), blank=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.title} - {self.category.category_name}'
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('comment', on_delete=models.CASCADE, null=True, related_name="replies")
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Subscribe(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'Subscribe'
        verbose_name_plural = 'Subscribes'    

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=500)
    message = models.TextField()
    msg_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Name- {self.name} and email- {self.email}'
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes_post')
    user_likes = models.ManyToManyField(User, blank=True)
    like_status = models.BooleanField(default=False)
    like_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post} likes'
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
    
