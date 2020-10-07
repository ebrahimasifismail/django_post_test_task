from datetime import datetime
from datetime import timedelta

from django.views import View
from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponse

from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.permissions import IsAuthenticated


from .serializers import PostImageSerializer, DislikeSerializer, LikeSerializer, PostSerializer, TagSerializer
from .models import PostImage, Dislike, Like, Post, Tag, UserPostWeight

from django.db.models import Prefetch, Count
# Create your views here.

class HomePageView(View):

    def get(self, request, *args, **kwargs):
        html = "<html><body>Successful .</body></html>" 
        return HttpResponse(html)


class PostImageViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    retrieve:
        Return a user instance.

    list:
        Return all users, ordered by most recently joined.

    create:
        Create a new user.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    update:
        Update a user.
    """
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = (IsAuthenticated, )



    def update(self, request, pk=None, *args, **kwargs):
        instance = self.queryset.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data)

class LikeAPIList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        post = Post.objects.filter(id=self.request.data['post'])
        if post:
            queryset = Like.objects.filter(user=self.request.user, post=post[0])
            if queryset.exists():
                if queryset[0].liked_status:
                    raise ValidationError('You have already liked')
                else:
                    queryset[0].liked_status = True
                    queryset[0].save()
            serializer.save(user=self.request.user)
            disliked = Dislike.objects.filter(user=self.request.user, post=post[0])
            if disliked:
                disliked[0].disliked_status = False
                disliked[0].save()
        else:
            raise ValidationError('Post Doesnot Exist')
 

class LikeAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class DislikeAPIList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer

    def perform_create(self, serializer):
        post = Post.objects.filter(id=self.request.data['post'])
        if post:
            queryset = Dislike.objects.filter(user=self.request.user, post=post[0])
            if queryset.exists():
                if queryset[0].disliked_status:
                    raise ValidationError('You have already disliked')
                else:
                    queryset[0].disliked_status = True
                    queryset[0].save()
            serializer.save(user=self.request.user)
            liked = Like.objects.filter(user=self.request.user, post=post[0])
            if liked:
                liked[0].liked_status = False
                liked[0].save()
        else:
            raise ValidationError('Post Doesnot Exist')

    

class DislikeAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer

class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    #queryset = Campaigns.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        liked_posts = Like.objects.filter(user=self.request.user)
        disliked = Dislike.objects.filter(user=self.request.user)
        if disliked:
            disliked_posts = Post.objects.filter(dislike__in=disliked)
            disliked_tags = Tag.objects.filter(tagssss__in=disliked_posts)
            excluded_posts =  list(Post.objects.exclude(tags__in=disliked_tags).distinct())
        else:
            excluded_posts = list(Post.objects.all())
        if liked_posts:

            user_prefernce = UserPostWeight.objects.filter(user=self.request.user)
            for prefered in user_prefernce:
                try:
                    excluded_posts[prefered.weight] = prefered.post
                except:
                    pass
            
            return excluded_posts
        else:
            return Post.objects.all()

    


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class TagList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer