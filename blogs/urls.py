from django.urls import path

from . import views

app_name = "blogs"
urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    path("<str:username>/posts/", views.user_post_list_view, name="user_posts"),
    path("new/", views.PostCreateView.as_view(), name="post_create"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail_view,
        name="post_detail",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/update/",
        views.post_update_view,
        name="post_update",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/delete/",
        views.post_delete_view,
        name="post_delete",
    ),
    path("tag/<slug:tag_slug>/", views.post_list_view, name="post_list_by_tag"),
]
