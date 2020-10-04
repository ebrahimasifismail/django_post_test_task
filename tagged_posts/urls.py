"""tagged_posts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.contrib import admin
from Posts import views
from tagged_posts import settings
from django.views.decorators.csrf import csrf_exempt

if "rest_framework_swagger" in settings.INSTALLED_APPS:
    from rest_framework_swagger.views import get_swagger_view
    schema_view = get_swagger_view(title="Tagged Posts APIs")

# from rest_framework import routers

# router = routers.DefaultRouter()

# router.register(r'get_members_by_username/', views.MembersViewSet, basename='MyModel')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Posts.urls')),
    path('test_view', view=csrf_exempt(views.HomePageView.as_view()), name='home')
]

if "django.contrib.admin" in settings.INSTALLED_APPS:
    #urlpatterns += [path("django-admin/", admin.site.urls)]

    urlpatterns += [path("docs/", schema_view)]

