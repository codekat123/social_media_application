from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
     path('sign-up/',SignUpView.as_view(),name='sign-up'),
     path('',login_user,name='login'),
     path('activation-account/<uid>/<token>/',activation_account,name='activation')
]