from django.shortcuts import render
#from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # 1. wymaga zalogowane urzytkownika, 2. wymaga aby dany urzytkownik który jest powiązany z daną operacją mógł ją wykonywać
from .models import Post, Comment

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog_app/home.html', context)

def about(request):
    return render(request, 'blog_app/about.html', {'title':'About'})


class PostListView(ListView):
    model = Post
    template_name = "blog_app/home.html" # I define my own path, default is: <app_name>/<model_used_lowercase>_<view_type>.html
    context_object_name = 'posts' # name which I use in .html
    ordering = ['-date_posted'] # post display order definition on the home site 



class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()[::-1]
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    # overwrite form_valid method
    def form_valid(self, form):
        form.instance.author = self.request.user # I define here who is the post author in the form which I try to submit.
        return super().form_valid(form) # after that above, I validate form


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    # overwrite form_valid method
    def form_valid(self, form):
        form.instance.author = self.request.user # I define here who is the post author in the form which I try to submit.
        return super().form_valid(form) # after that above, I validate form

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # tutaj nas przekieruje po usunięciu

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "blog_app/add_comment.html"
    fields = ['comm_content']

    # overwrite form_valid method
    def form_valid(self, form):
        #post = Post.objects.get(id=1)
        form.instance.post = Post.objects.get(id=self.kwargs.get('pk'))
        form.instance.author = self.request.user 
        return super().form_valid(form) 


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    # if you don't want to send POST request, you can use:
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

