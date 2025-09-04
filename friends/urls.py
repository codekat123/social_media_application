from django.urls import path
from .views import *

app_name = "friends"

urlpatterns = [
     path('settings/',AccountSettingsView.as_view(),name='profile'),
]