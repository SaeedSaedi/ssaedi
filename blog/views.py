from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag


# Create your views here.
def index(request):
    category = request.GET.get("category")
    tag = request.GET.get("tag")

    posts = Post.objects.filter(status="published")

    if category:
        try:
            category = Category.objects.get(name=category)
            posts = posts.filter(category=category)
        except Category.DoesNotExist:
            posts = Post.objects.none()

    if tag:
        try:
            tag = Tag.objects.get(name=tag)
            posts = posts.filter(tags=tag)
        except Tag.DoesNotExist:
            posts = Post.objects.none()

    return render(request, "index.html", context={"posts": posts})


def contact(request):
    return render(request, "contactus.html")


def post_single(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="Published")

    post.counted_views += 1
    post.save()

    context = {
        "post": post,
    }

    return render(
        request,
        "blog-single.html",
        context=context,
    )
