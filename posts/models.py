from django.db import models
from accounts.models import User

class Post(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')
     image = models.ImageField(upload_to='posts',null=True,blank=True)
     caption = models.TextField(max_length=400)
     create_at = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
          return self.user.username
