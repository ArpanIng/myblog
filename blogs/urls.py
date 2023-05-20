from django.urls import path

from . import views

app_name = "blogs"
urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail_view,
        name="post_detail",
    ),
    path("<int:post_id>/share/", views.post_share_view, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment_view, name="post_comment"),
    path("tag/<slug:tag_slug>/", views.post_list_view, name="post_list_by_tag"),
    path("test", views.test),
]
