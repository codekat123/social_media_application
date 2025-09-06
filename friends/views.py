from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.contrib import messages
from accounts.models import User
from friends.models import Friend
from .forms import ModifyUserForm
from posts.models import Post

@method_decorator(login_required(login_url='accounts:login'),name='dispatch')
class AccountSettingsView(UpdateView):
     model = User
     form_class = ModifyUserForm  
     template_name = 'friend/settings.html'
     success_url = '/friend/profile/'
     
     def get_object(self,queryset=None):
          return self.request.user
     
class FriendMixin:
     def get_friend(self,id=None,username=None):
          if id:
               return get_object_or_404(User,id=id)
          elif username:
               return get_object_or_404(User,username=username)
     
     def get_follow_data(self,user):
          return {
               'followers': Friend.objects.filter(user_B=user).count(),
               'following': Friend.objects.filter(user_A=user).count(),
          }
   
@method_decorator(login_required(login_url='accounts:login'),name='dispatch')
class Profile(FriendMixin,ListView):
     model = User
     template_name = 'friend/profile.html'
     paginate_by = 2
     def get_context_data(self,*,object_list=None,**kwargs):
          context = super().get_context_data(**kwargs)
          context.update(self.get_follow_data(self.request.user))
          return context
     def get_queryset(self):
          return Post.objects.filter(user=self.request.user).order_by('-create_at')

class ProfileFriend(FriendMixin,ListView):
     model = User
     template_name = 'friend/profile_friend.html'
     paginate_by = 2

     def get_context_data(self,*,object_list=None,**kwargs):
          context = super().get_context_data(**kwargs)
          username = self.kwargs['username']
          friend = self.get_friend(username=username)
          context.update(self.get_follow_data(friend))
          existing = Friend.objects.filter(user_A=self.request.user,user_B=friend).exists()
          context['existing'] = existing
          context['friend'] = friend
          return context
     
     def get_queryset(self):
          username = self.kwargs['username']
          friend = self.get_friend(username=username)
          return Post.objects.filter(user=friend).order_by('-create_at')


def follow(request,friend_id):
     mixin = FriendMixin()
     friend = mixin.get_friend(id=friend_id)
     user = request.user
     existing = Friend.objects.filter(user_A=user,user_B=friend).exists()
     if friend == user:
          messages.error(request,'you cannot add yourself as friend')
     elif existing:
          messages.info(request,"you're already friends ")
     else:
          user = Friend.objects.create(user_A=user,user_B=friend)
          user.save()
     return redirect('friends:friend',username=friend.username)


def unfollow(request,friend_id):
     mixin = FriendMixin()
     friend = mixin.get_friend(id=friend_id)
     user = request.user
     relationship = get_object_or_404(Friend,user_A=user,user_B=friend)
     relationship.delete()
     return redirect('friends:friend',username=friend.username)

class SearchFriend(ListView):
     model = User
     template_name = 'friend/search_friend.html'
     paginate_by = 2

     def get_queryset(self):
          search = self.request.GET.get('q','')
          results = User.objects.filter(username__contains=search)
          return results
     