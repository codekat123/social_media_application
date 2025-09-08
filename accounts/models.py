from django.db import models
from django.contrib.auth.models import AbstractUser
import pycountry
from friends.models import Friend

class User(AbstractUser):
     @staticmethod
     def get_country():
          countries = list(pycountry.countries)
          country = [(country.alpha_2,country.name) for country in countries]
          return country
     bio = models.TextField(max_length=300,null=True,blank=True)
     cover_photo = models.ImageField(upload_to='profile',default='profile/default.jpeg')
     date_of_birthday = models.DateField(null=True,blank=True)
     website = models.URLField(null=True,blank=True)
     country = models.CharField(max_length=100, blank=True, choices=get_country())

     def __str__(self):
          return self.username
     
     def get_num_posts(self):
          return self.post.all().count()
     
     def get_following(self):
          return Friend.objects.filter(user_A=self).values_list("user_B_id", flat=True)
