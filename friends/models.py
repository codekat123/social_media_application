from django.db import models


class Friend(models.Model):
     user_A = models.ForeignKey("accounts.User",on_delete=models.CASCADE,related_name='user_A')
     user_B = models.ForeignKey("accounts.User",on_delete=models.CASCADE,related_name='user_B')

     def __str__(self):
          return self.user_A.username +"--->"+ self.user_B.username