from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.
def index(request):
    posts = Post.objects.filter(status="Published")

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
