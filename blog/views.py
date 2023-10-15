from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import CommentForm


def index(request):
    return render(request, 'index.html')


class PostListView(generic.ListView):
    model = Post
    ordering = ['-created_on']
    context_object_name = 'posts'
    template_name = "post_list.html"
    # template_name = "index.html"
    paginate_by = 6


class PostDetailView(generic.DetailView):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                "comment_form": CommentForm()
            },
        )
