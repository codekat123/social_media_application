from django.urls import path
from .views import *

app_name = "posts"

urlpatterns = [
               path('create-post/',CreatePost.as_view(),name='create'),
               path('update-post/<int:pk>/',UpdatePost.as_view(),name='update'),
               path('delete-post/<int:pk>/',PostDeleteView.as_view(),name='delete'),
               path('home/',HomePage.as_view(),name='home'),
]