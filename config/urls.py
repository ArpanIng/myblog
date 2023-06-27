from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from blogs.views import post_list_view, AboutView
from blogs.feeds import PostsFeeds, AtomSiteNewsFeed
from blogs.sitemaps import PostSitemap

sitemaps = {
    "posts": PostSitemap,
}

context = {
    "sitemaps": sitemaps,
}

urlpatterns = [
    path("", post_list_view, name="post_list"),
    path("about/", AboutView.as_view(), name="about"),
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls", namespace="accounts")),
    path("blog/", include("blogs.urls")),
    path("feed/rss", PostsFeeds(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("sitemap.xml", sitemap, context, name="django.contrib.sitemaps.views.sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
