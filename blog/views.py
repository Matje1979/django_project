from __future__ import print_function
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, Image
from users.models import Profile
from .forms import CommentForm




def home(request):
    context = {
        'posts': Post.objects.all()
    }
               
    return render(request, 'blog/home.html', context)
    #return HttpResponse('<h1>Blog Home</h1>')
    
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    

class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class ProfileDetailView(DetailView):
    model = Profile

def about(request, id):
    obj = get_object_or_404(Profile, id=id)
    context = { "object": obj }
    return render(request, 'users/profile_detail.html', context)
    #return HttpResponse('<h1>Blog About</h1>')
    
def post_detail(request, id):
    obj = get_object_or_404(Post, id=id)
    if request.method == "POST":
        comment = CommentForm(request.Post)
        if comment.is_valid:
            comment.save()
            comments = Comment.objects.filter(post = obj).all()
            context = { "object": obj, "comments" : comments }
            return (request, 'blog/post_detail.html', context)
            
    else:
        comment_form = CommentForm()
        comments = Comment.objects.all()
        context = { "object": obj, "comments" : comments, "c_form": comment_form }
    return render(request, 'blog/post_detail.html', context)

def image_list(request):
    images = Image.objects.all()
    context = {'images': images}
    return render(request, 'blog/galery.html', context)
    
    
