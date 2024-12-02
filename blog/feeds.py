from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "Latest Blog Posts"
    link = "/feed/"
    description = "Updates on the latest blog posts."

    def items(self):
        return Post.objects.filter(status="published").order_by("-created_at")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:100]

    def item_link(self, item):
        return reverse("blog:post_detail", args=[item.pk])
