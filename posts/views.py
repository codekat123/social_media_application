from django.shortcuts import render , get_object_or_404 , redirect
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Post
from django.urls import reverse_lazy

@method_decorator(login_required(login_url='accounts:login'),name='dispatch')
class CreatePost(CreateView):
     model = Post
     fields = ['caption','image']
     template_name = 'posts/create_post.html'
     success_url = '/friend/profile/'

     def form_valid(self,form):
          form.instance.user = self.request.user
          return super().form_valid(form)

@method_decorator(login_required(login_url='accounts:login'),name='dispatch')
class UpdatePost(UpdateView):
     model = Post
     fields = ['image','caption']
     template_name = 'posts/update.html'
     success_url ='/friend/profile/'
     
@method_decorator(login_required(login_url='accounts:login'),name='dispatch')
class PostDeleteView(DeleteView):
     model = Post
     success_url = reverse_lazy('friends:profile')
     template_name = 'posts/delete.html'

     def get_queryset(self):
          return super().get_queryset().filter(user=self.request.user )

@method_decorator(login_required(login_url='accounts:login'),name='dispatch')
class HomePage(ListView):
     model = Post
     template_name = 'posts/home.html'
     paginate_by = 5

     def get_queryset(self):
          following = self.request.user.get_following()
          return Post.objects.filter(user__in=following)