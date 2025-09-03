from django.db import models
from django.contrib.auth.models import User
import pycountry

class Profile(models.Model):
     @staticmethod
     def get_country():
          countries = list(pycountry.countries)
          country = [(country.alpha_2,country.name) for country in countries]
          return country

     user = models.ForeignKey(User,on_delete=models.CASCADE)
     bio = models.TextField(max_length=300)
     cover_photo = models.ImageField(upload_to='profile',default='profile/default.jpeg')
     profile_picture = models.ImageField(upload_to='profile',null=True,blank=True)
     date_of_birthday = models.DateField(null=True,blank=True)
     website = models.URLField(blank=True)
     country = models.CharField(max_length=100, blank=True, choices=get_country())
     joined_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
          return self.user.username