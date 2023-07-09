from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from .forms import PostModelForm, CommentModelForm
from .models import Post

User = get_user_model()


def search_form(request):
    if request.GET.get("q") == None:
        q = ""
    else:
        q = request.GET.get("q")
    # user can search blog post by title
    results = Post.objects.filter(title__icontains=q)
    return render(request, "blogs/search.html", {"results": results})


def post_list_view(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, per_page=5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    context = {
        "posts": posts,
    }
    return render(request, "blogs/post_list.html", context)


def user_post_list_view(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.published.filter(author=user).order_by("-updated")
    paginator = Paginator(post_list, per_page=5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    context = {
        "user": user,
        "posts": posts,
    }
    return render(request, "blogs/user_posts.html", context)


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    form_class = PostModelForm
    success_message = "The post has been created successfully."
    template_name = "blogs/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentGetView(generic.DetailView):
    context_object_name = "post"
    template_name = "blogs/post_detail.html"

    def get_object(self):
        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs["post_slug"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # list of active comments for a post
        comments = post.comments.filter(active=True)
        context["comments"] = comments
        context["form"] = CommentModelForm()
        return context


class CommentPostView(SingleObjectMixin, generic.FormView):
    form_class = CommentModelForm
    template_name = "blogs/post_detail.html"

    def get_object(self):
        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs["post_slug"],
        )

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.get_object()
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse("blogs:post_detail", kwargs={"post_slug": post.slug})


class PostDetailView(generic.DetailView):
    def get(self, request, *args, **kwargs):
        view = CommentGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPostView.as_view()
        return view(request, *args, **kwargs)


class PostUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView
):
    context_object_name = "post"
    form_class = PostModelForm
    success_message = "The post has been updated successfully."
    template_name = "blogs/post_update.html"

    def get_object(self):
        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs["post_slug"],
        )

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView
):
    context_object_name = "post"
    success_message = "The post has been deleted successfully."
    success_url = reverse_lazy("blogs:post_list")
    template_name = "blogs/post_delete.html"

    def get_object(self):
        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs["post_slug"],
        )

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class AboutView(generic.TemplateView):
    template_name = "about.html"
