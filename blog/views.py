from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from .models import Post, Profile
from .forms import CommentForm, EditUserForm, EditProfileForm


def index(request):
    return render(request, 'index.html')


class PostListView(generic.ListView):
    model = Post
    ordering = ['-created_on']
    context_object_name = 'posts'
    template_name = "post_list.html"
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
