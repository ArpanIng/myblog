from django.urls import path

from . import views

app_name = "blogs"
urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    path("<str:username>/posts/", views.user_post_list_view, name="user_posts"),
    path("new/", views.PostCreateView.as_view(), name="post_create"),
    path("search/", views.search_form, name="search"),
    path(
        "<slug:post_slug>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "<slug:post_slug>/update/",
        views.PostUpdateView.as_view(),
        name="post_update",
    ),
    path(
        "<slug:post_slug>/delete/",
        views.PostDeleteView.as_view(),
        name="post_delete",
    ),
]
