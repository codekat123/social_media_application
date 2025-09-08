from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic.edit import CreateView
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
from .forms import SignUpForm , ForgetPassword , EnterNewPassword
from django.contrib import messages



class SignUpView(CreateView):
     model = User
     form_class = SignUpForm
     template_name = 'accounts/signup.html'

     def form_valid(self,form):
          user = form.save(commit=True)
          user.is_active = False
          user.save()
          domain = get_current_site(self.request).domain
          uid = urlsafe_base64_encode(force_bytes(user.pk))
          token =default_token_generator.make_token(user)
          mail_subject = f'please active your account'
          activation_link = f'http://{domain}{reverse('accounts:activation',args=[uid,token])}'
          context = {
               'user':user,
               'activation_link':activation_linkd
          }
          message = render_to_string('accounts/verification_email.html',context)

          mail = EmailMultiAlternatives(mail_subject,message,settings.DEFAULT_FROM_EMAIL,[user.email])
          mail.attach_alternative(message, "text/html")
          mail.send()
          messages.success(self.request,"please check your email to active your account")
          return redirect('accounts:login')
     
     def get(self,*args,**kwargs):
          if self.request.user.is_authenticated:
               return redirect('posts:home')
          return super(SignUpView,self).get(*args,**kwargs)
     
def activation_account(request,uid,token):
     id = urlsafe_base64_decode(uid).decode()
     user = get_object_or_404(User,id=id)
     
     if user is not None and default_token_generator.check_token(user,token):
          user.is_active = True
          user.save()
          messages.success(request,"your account has been activated")
          return redirect('accounts:login')
     else:
          messages.error(request,"something went wrong")
          return redirect('sign-up') 
     

def login_user(request):
     if request.user.is_authenticated:
          return redirect('posts:home')
     if request.method == "POST":
          username = request.POST.get('username')
          password = request.POST.get('password')
          
          user = authenticate(request,username=username,password=password)
          if user is not None:
               login(request,user)
               return redirect('posts:home')
          else:
               try:
                    user = User.objects.get(username=username)
                    if not user.is_active:
                         messages.warning(request,"please active your account ")
                    return redirect('accounts:login')
               except User.DoesNotExist:
                    messages.error(request,'the password or username are wrong')
                    return redirect('accounts:login')
     else:
          return render(request,'accounts/login.html')
     
def logout_user(request):
     logout(request)
     return redirect('accounts:login')


def forget_password(request):
    if request.method == 'POST':
        form = ForgetPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                subject = "Reset your password"
                domain = get_current_site(request).domain
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                link_activation = f"http://{domain}{reverse('accounts:reset_password', args=[uid, token])}"

                context = {
                    'user': user,
                    'link': link_activation,
                }
                message = render_to_string('accounts/email_reset_password.html', context)

                mail = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                mail.attach_alternative(message, "text/html")
                mail.send()

            messages.warning(request, 'If this email exists, you’ll receive a reset link.')
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/reset_password.html', {'form': form})
    else:
        form = ForgetPassword()

    return render(request, 'accounts/reset_password.html', {'form': form})



def reset_password(request, uid, token):
    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = get_object_or_404(User, id=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = EnterNewPassword(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                messages.success(request, 'Password has been changed successfully')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Something went wrong')
        else:
            form = EnterNewPassword()

        return render(request, 'accounts/reset.html', {'form': form})

    messages.error(request, "Reset link is invalid or expired")
    return redirect('accounts:forget_password')

               