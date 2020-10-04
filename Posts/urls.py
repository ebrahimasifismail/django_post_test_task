from django.urls import include, path
from rest_framework import routers
from collections import OrderedDict, namedtuple

from . import views
    

router = routers.SimpleRouter()




router.register(r'postimages', views.PostImageViewSet, basename='MyModel')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path("", include("rest_auth.urls")),
    path('post_list_create/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('tag_list_create/', views.TagList.as_view()),
    path('tag/<int:pk>/', views.TagDetail.as_view()),
    path('like_list_create/', views.LikeAPIList.as_view()),
    path('like/<int:pk>/', views.LikeAPIDetail.as_view()),
    path('dislike_list_create/', views.DislikeAPIList.as_view()),
    path('dislike_list_create/<int:pk>/', views.DislikeAPIDetail.as_view()),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    
]
