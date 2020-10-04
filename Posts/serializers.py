from rest_framework import serializers
from django.contrib.auth.models import User
from rest_auth.serializers import LoginSerializer as BaseLoginSerializer

from .models import PostImage, Like, Dislike, Post, Tag

class PostImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name =  serializers.CharField(max_length=1000, allow_blank=True, allow_null=True)
    image_url = serializers.CharField(max_length=1000, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return PostImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()
        return instance

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        # fields = ('id', 'lead_name', 'profile_picture', 'occupation', 'location', 'linkedin_url')
        fields = '__all__'
        read_only_fields = ("user",)


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        # fields = ('id', 'lead_name', 'profile_picture', 'occupation', 'location', 'linkedin_url')
        fields = '__all__'
        read_only_fields = ("user",)

class PostSerializer(serializers.ModelSerializer):
    liked_status = serializers.SerializerMethodField(read_only=True)
    disliked_status = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    dislikes_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        # fields = ('id', 'lead_name', 'profile_picture', 'occupation', 'location', 'linkedin_url')
        fields = '__all__'    
        
        
    def get_liked_status(self, obj):
        current_user = self.context['request'].user
        liked_list = Like.objects.filter(user=current_user, post=obj)
        if not liked_list:
            return False
        elif liked_list[0].liked_status:
            return True
        else: 
            return False

    def get_disliked_status(self, obj):
        current_user = self.context['request'].user
        disliked_list = Dislike.objects.filter(user=current_user, post=obj)
        if not disliked_list:
            return False
        elif disliked_list[0].disliked_status:
            return True
        else: 
            return False
    
    def get_likes_count(self, obj):
        current_user = self.context['request'].user
        liked_list = Like.objects.filter(post=obj)
        if liked_list:
            return int(len(liked_list))
        else: 
            return None

    def get_dislikes_count(self, obj):
        current_user = self.context['request'].user
        disliked_list = Dislike.objects.filter(post=obj)
        if disliked_list:
            return int(len(disliked_list))
        else: 
            return None 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = ('id', 'lead_name', 'profile_picture', 'occupation', 'location', 'linkedin_url')
        fields = '__all__'


class LoginSerializer(BaseLoginSerializer):
    # make email mandatory
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)