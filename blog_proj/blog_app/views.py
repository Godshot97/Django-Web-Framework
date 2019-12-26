from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from .models import Post, Comment
from django.contrib.auth.models import User
import datetime

def about(request):
    return render(request, 'blog_app/about.html', {'title':'About'})


class PostListView(ListView):
    model = Post
    template_name = "blog_app/home.html" 
    context_object_name = 'posts' 
    #ordering = ['-date_posted'] 
    paginate_by = 4

    def get_queryset(self):
        search1 = self.request.GET.get('date_filter1', None) 
        search2 = self.request.GET.get('date_filter2', None)
        
        if (search1 is not None) and (search2 is not None) and (search1 != '') and (search2 != ''):
            search2 = datetime.datetime.strptime(search2, "%Y-%m-%d")
            search2 += datetime.timedelta(days=1)
            search2 = search2.strftime("%Y-%m-%d")
            return Post.objects.filter(date_posted__range=[search1, search2]).order_by('-date_posted')
        else:
            return Post.objects.all().order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = "blog_app/user_posts.html" 
    context_object_name = 'posts' 
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        search1 = self.request.GET.get('date_filter1', None) 
        search2 = self.request.GET.get('date_filter2', None)
        
        if (search1 is not None) and (search2 is not None) and (search1 != '') and (search2 != ''):
            search2 = datetime.datetime.strptime(search2, "%Y-%m-%d")
            search2 += datetime.timedelta(days=1)
            search2 = search2.strftime("%Y-%m-%d")
            return Post.objects.filter(author=user).filter(date_posted__range=[search1, search2]).order_by('-date_posted')
        else:
            return Post.objects.filter(author=user).order_by('-date_posted') 

        

class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()[::-1]
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    # overwrite form_valid method
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form) 


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    # overwrite form_valid method
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form) 

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' 

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "blog_app/add_comment.html"
    fields = ['comm_content']

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs.get('pk'))
        form.instance.author = self.request.user 
        return super().form_valid(form) 


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

