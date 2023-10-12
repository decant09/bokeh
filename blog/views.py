from django.shortcuts import render
from django.views import generic
from .models import Post


class PostListView(generic.ListView):
    model = Post
    ordering = ['-created_on']
    template_name = "index.html"
    paginate_by = 6
