from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from blogs.sitemaps import PostSitemap

sitemaps = {
    "posts": PostSitemap,
}

context = {
    "sitemaps": sitemaps,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blogs.urls")),
    path("sitemap.xml", sitemap, context, name="django.contrib.sitemaps.views.sitemap"),
]
