from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
class SignUpForm(UserCreationForm):
     class Meta:
          model = User
          fields = ['username','email','password1','password2']

class ForgetPassword(forms.Form):
    email = forms.EmailField(
        max_length=60,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter your email address",
                "id": "email-field"
            }
        )
    )

class EnterNewPassword(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "w-full border rounded-lg p-2"}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "w-full border rounded-lg p-2"}),
        label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data