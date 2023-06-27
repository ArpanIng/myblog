import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class PostsFeeds(Feed):
    title = "My post"
    link = reverse_lazy("blogs:post_list")
    description = "New posts of MyBlog."

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_lastupdated(self, item):
        return item.updated


class AtomSiteNewsFeed(PostsFeeds):
    feed_type = Atom1Feed
    subtitle = PostsFeeds.description
