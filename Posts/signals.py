from django.db.models import signals
from django.dispatch import receiver

from .models import Like, Dislike, UserPostWeight, Post


@receiver(signals.post_save, sender=Like)
def order_posts_to_likes(sender, instance, created=False, **kwargs):
    """
    Creates invoice document's root folder.
    """
    user = instance.user
    post = instance.post
    tags = post.tags.all()

    likes = Like.objects.filter(user=user, post=post)
    liked_posts = [ i.post for i in likes if i.liked_status==True]

    for post in liked_posts:
        liked_tags = post.tags.all()
        for tag in liked_tags:
            if not tag in tags:
                tags.append(tag)

    similar_posts = Post.objects.filter(tags__in=tags).distinct()
    try:
        UserPostWeight.objects.filter(user=user).delete()
    except:
        pass
    weight = 2
    for post in similar_posts:
        UserPostWeight.objects.create(user=user, post=post, weight=weight)
        weight+=2
    


    pass