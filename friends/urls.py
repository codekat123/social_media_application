from django.urls import path
from .views import *

app_name = "friends"

urlpatterns = [
     path('settings/',AccountSettingsView.as_view(),name='settings'),
     path('profile/',Profile.as_view(),name='profile'),
     path('profile/<str:username>/',ProfileFriend.as_view(),name='friend'),
     path('follow/<int:friend_id>/',follow,name='follow'),
     path('unfollow/<int:friend_id>/',unfollow,name='unfollow'),
     path('search/',SearchFriend.as_view(),name='search')
]