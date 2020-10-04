from django.contrib import admin
from .models import PostImage, Tag, Post, Like, Dislike, UserPostWeight
# Register your models here.


admin.site.register(PostImage)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(UserPostWeight)