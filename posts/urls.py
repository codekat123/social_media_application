from django.urls import path
from .views import *

app_name = "posts"

urlpatterns = [
               path('create-post/',CreatePost.as_view(),name='create'),
]