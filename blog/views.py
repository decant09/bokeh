from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic, View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Post, Profile, Comment
from .forms import CommentForm, EditUserForm, EditProfileForm, PostForm


def index(request):
    return render(request, 'index.html')


class PostListView(generic.ListView):
    model = Post
    ordering = ['-created_on']
    context_object_name = 'posts'
    template_name = "post_list.html"
    paginate_by = 6


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,
                        request.FILES
                        )
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(
                request,
                'Thanks for contributing. Your post was created successfully'
            )
            return redirect('post-detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'image']
    template_name = 'post_edit.html'

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy('post-detail', kwargs={'slug': slug})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Your post was updated successfully'
        )
        return response


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Your post was deleted successfully")
        return reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


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
                'commented': False,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.u_name = request.user
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request,
                             'Comment posted successfully. Awaiting approval.')
        else:
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': True,
                "comment_form": CommentForm()
            },
        )


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        slug = self.kwargs['slug']
        messages.success(self.request, "Your comment was deleted successfully")
        return reverse_lazy('post-detail', kwargs={'slug': slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.u_name


@login_required
def profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        edit_user = EditUserForm(request.POST, instance=request.user)
        edit_profile = EditProfileForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile)
        if edit_user.is_valid() and edit_profile.is_valid():
            edit_user.save()
            edit_profile.save()
            messages.success(request, f'Profile updated successfully')
            return redirect('profile')
    else:
        profile = Profile.objects.get(user=request.user)
        edit_user = EditUserForm(instance=request.user)
        edit_profile = EditProfileForm(instance=request.user.profile)

    context = {
        'profile': profile,
        'edit_user': edit_user,
        'edit_profile': edit_profile
    }
    return render(request, 'profile.html', context)
