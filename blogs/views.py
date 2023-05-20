from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from taggit.models import Tag

from .forms import EmailPostForm, CommentModelForm
from .models import Post, Comment


def post_list_view(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get("page")
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(number=1)

    context = {
        "posts": posts,
        "tag": tag,
    }
    return render(request, "blogs/test_list.html", context)


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
    form = CommentModelForm()

    # list of similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "similar_posts": similar_posts,
    }
    return render(request, "blogs/test_detail.html", context)


def post_share_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            from_email = "ingnamarpan@gmail.com"
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=["ingnamarpan@gmail.com"],
                fail_silently=True,
            )
            sent = True
    else:
        form = EmailPostForm()

    context = {
        "form": form,
        "post": post,
        "sent": sent,
    }
    return render(request, "blogs/share.html", context)


@require_POST  # shortcut for if request.method == 'POST'
def post_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentModelForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        "form": form,
        "post": post,
        "comment": comment,
    }
    return render(request, "blogs/comment.html", context)


def test(request):
    return render(request, "test_base.html")
