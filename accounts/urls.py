from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
     path('sign-up/',SignUpView.as_view(),name='sign-up'),
     path('',login_user,name='login'),
     path('activation-account/<uid>/<token>/',activation_account,name='activation'),
     path('logout/',logout_user,name='logout'),
     path('forget-password/',forget_password,name='forget_password'),
     path('reset-password/<uid>/<token>/',reset_password,name='reset_password'),
]