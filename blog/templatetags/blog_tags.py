from django import template
from django.utils import timezone
from datetime import timedelta
from blog.models import Post, Category

register = template.Library()


@register.simple_tag(name="get_current_time")
def get_current_time():
    now = timezone.now()
    return now.strftime("%d %B, %Y, %H:%M")


@register.simple_tag(name="get_trends")
def get_trends():
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)

    top_posts = Post.objects.filter(
        created_at__gte=twenty_four_hours_ago, status="published"
    ).order_by("-counted_views")[:4]

    return top_posts


@register.simple_tag(name="get_top_posts")
def get_top_posts():
    top_posts = Post.objects.filter(status="published").order_by("-counted_views")[:4]

    return top_posts


@register.simple_tag(name="get_last_posts")
def get_last_posts(n=3):

    last_posts = Post.objects.filter(status="published").order_by("-created_at")[:n]

    return last_posts


@register.simple_tag(name="get_category_counts")
def get_category_counts():

    categories = Category.objects.all()
    category_counts = {}
    for category in categories:

        post_count = Post.objects.filter(category=category, status="published").count()
        category_counts[category.name] = post_count

    return category_counts
