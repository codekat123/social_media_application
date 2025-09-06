from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Post


@method_decorator(login_required(login_url='accounts:login'),name='dispatch')
class CreatePost(CreateView):
     model = Post
     fields = ['caption','image']
     template_name = 'posts/create_post.html'
     success_url = '/friend/profile/'

     def form_valid(self,form):
          form.instance.user = self.request.user
          return super().form_valid(form)
