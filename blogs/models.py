from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """
    Custom Manager
    Returns: Post with 'PUBLISHED' status
    """

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # default Manager
    published = PublishedManager()  # custom Manager
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def get_absolute_url(self):
        return reverse(
            "blogs:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"
