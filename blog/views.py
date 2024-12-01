from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category, Tag, User
from blog.forms import NewsletterForm
from django.contrib import messages


# Create your views here.
def index(request):
    category = request.GET.get("category")
    tag = request.GET.get("tag")
    author = request.GET.get("author")

    posts = Post.objects.filter(status="published")

    if author:
        try:
            author = User.objects.get(username=author)
            posts = posts.filter(author=author)
        except User.DoesNotExist:
            posts = Post.objects.none()

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

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect("blog:index")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, "index.html", context={"posts": posts})


def blog_search(request):
    search_query = request.GET.get("q", "")
    posts = Post.objects.filter(status="published", content__icontains=search_query)

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
