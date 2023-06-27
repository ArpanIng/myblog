from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

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
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page")
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(number=1)

    context = {
        "user": user,
        "posts": posts,
    }
    return render(request, "blogs/user_posts.html", context)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostModelForm
    template_name = "blogs/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )

    # list of active comments for a post
    comments = post.comments.filter(active=True)

    if request.method == "POST":
        form = CommentModelForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(
                "blogs:post_detail",
                post.publish.year,
                post.publish.month,
                post.publish.day,
                post.slug,
            )
    else:
        form = CommentModelForm()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blogs/post_detail.html", context)


@login_required
def post_update_view(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )

    if request.user != post.author:
        return HttpResponse("Forbidden! Access not granted.")

    if request.method == "POST":
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(
                "blogs:post_detail",
                post.publish.year,
                post.publish.month,
                post.publish.day,
                post.slug,
            )
    form = PostModelForm(instance=post)

    context = {
        "post": post,
        "form": form,
    }
    return render(request, "blogs/post_update.html", context)


@login_required
def post_delete_view(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )

    if request.user != post.author:
        return HttpResponse("Forbidden! Access not granted.")

    if request.method == "POST":
        post.delete()
        return redirect("blogs:post_list")

    context = {
        "post": post,
    }
    return render(request, "blogs/post_delete.html", context)


def about_view(request):
    return render(request, "about.html")
