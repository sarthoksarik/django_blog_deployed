from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Announcements


# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# view for announcement


def announcements(request):

    announce_objects = Announcements.objects.all()

    # reverse order the announcements according to datetime
    reversed_announcements = sorted(
        announce_objects, key=lambda item: item.date_created, reverse=True)

    context = {
        'announcements': reversed_announcements,
        'title': 'Announcements'
    }
    return render(request, 'blog/announcements_list.html', context)


@login_required
def upvote_post(request):

    if request.method == 'POST':

        post_id = int(request.POST["post_id"])

        post = get_object_or_404(Post, pk=post_id)

        try:

            user = request.user
            if user in post.upvotes.all():
                post.upvotes.remove(user)
            else:
                post.upvotes.add(user)
            # (request.META.get('HTTP_REFERER'))
            # (HttpResponseRedirect(request.META.get('HTTP_REFERER')))

            return HttpResponse("updated")

        except:
            return HttpResponseRedirect(reverse('blog-home'))
    else:
        return HttpResponseRedirect(reverse('blog-home'))
