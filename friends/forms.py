from django import forms
from accounts.models import User

class ModifyUserForm(forms.ModelForm):
     class Meta:
          model = User
          fields = ['first_name','last_name','country','website','cover_photo','date_of_birthday','bio']

     def __init__(self, *args, **kwargs):
        super(ModifyUserForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birthday'].widget.attrs.update({
            'type': 'date',  
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Select your birthday'
        })