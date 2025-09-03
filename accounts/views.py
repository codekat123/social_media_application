from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic.edit import CreateView , UpdateView
from django.contrib.auth import logout , login , authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from .models import User
from .forms import SignUpForm
from django.contrib import messages
class SignUpView(CreateView):
     model = User
     form_class = SignUpForm
     template_name = 'accounts/signup.html'

     def form_valid(self,form):
          user = form.save(commit=True)
          user.is_active = False
          user.save()
          domain = get_current_site(self.request)
          uid = urlsafe_base64_encode(force_bytes(user.pk))
          token =default_token_generator.make_token(user)
          mail_subject = f'please active your account'
          activation_link = f'http://{domain}{reverse('accounts:activation',args=[uid,token])}'
          context = {
               'user':user,
               'activation_link':activation_link
          }
          message = render_to_string('accounts/verification_email.html',context)

          mail = EmailMultiAlternatives(mail_subject,message,settings.DEFAULT_FROM_EMAIL,[user.email])
          mail.attach_alternative(message, "text/html")
          mail.send()
          messages.success(self.request,"please check your email to active your account")
          return redirect('accounts:login')
     
     def get(self,*args,**kwargs):
          if self.request.user.is_authenticated:
               return redirect('/')
          return super(SignUpView,self).get(*args,**kwargs)
     
def activation_account(request,uid,token):
     id = urlsafe_base64_decode(uid).decode()
     user = get_object_or_404(User,id=id)
     
     if user is not None and default_token_generator.check_token(user,token):
          user.is_active = True
          user.save()
          return redirect('accounts:login')
     else:
          return redirect('sign-up') 
     

def login_user(request):
     if request.method == "POST":
          username = request.POST.get('username')
          password = request.POST.get('password')
          
          user = authenticate(username=username,password=password)
          if user is not None:
               login(request,user)
               return redirect('accounts:profile')
          else:
               print('error')
               return redirect('accounts:login')
     else:
          return render(request,'accounts/login.html')
     
def logout_user(request):
     logout(request.user)
     return redirect('accounts:login')