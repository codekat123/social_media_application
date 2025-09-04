from django.shortcuts import render
from django.views.generic.edit import UpdateView
from accounts.models import User

class AccountSettingsView(UpdateView):
     model = User
     template_name = 'friend/settings.html'
     fields = ['first_name','last_name','country','website','cover_photo','date_of_birthday',]
     success_url = '/profile/'
     
     def get_object(self,queryset=None):
          return self.request.user
     

