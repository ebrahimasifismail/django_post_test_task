from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PostImage(models.Model):
    name =  models.CharField(max_length=1000, blank=True, null=True)
    image_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    images = models.ManyToManyField(PostImage)
    tags = models.ManyToManyField(Tag, related_name="tagssss")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, verbose_name=("liked_user"), on_delete=models.CASCADE)
    post = models.ForeignKey("Post", verbose_name=("liked_post"), on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    liked_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + ' ' + self.post.title

class Dislike(models.Model):
    user = models.ForeignKey(User, verbose_name=("liked_user"), on_delete=models.CASCADE)
    post = models.ForeignKey("Post", verbose_name=("liked_post"), on_delete=models.CASCADE)
    disliked_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    disliked_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + ' ' + self.post.title


class UserPostWeight(models.Model):
    user = models.ForeignKey(User, verbose_name=("liked_user"), on_delete=models.CASCADE)
    post = models.ForeignKey("Post", verbose_name=("liked_post"), on_delete=models.CASCADE)
    weight = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.email + ' ' + self.post.title
