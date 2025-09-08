from django import forms
from accounts.models import User

class ModifyUserForm(forms.ModelForm):
     class Meta:
          model = User
          fields = ['first_name','last_name','country','website','cover_photo','date_of_birthday','bio']
