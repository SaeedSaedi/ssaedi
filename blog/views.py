from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category, Tag, User, Comment
from blog.forms import NewsletterForm, PostForm, CommentForm, ContactForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


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

    posts = Paginator(posts, 4)
    page_number = request.GET.get("page", 1)
    posts = posts.get_page(page_number)

    return render(request, "index.html", context={"posts": posts, "title": "Home"})


def blog_search(request):
    search_query = request.GET.get("q", "")
    posts = Post.objects.filter(status="published", content__icontains=search_query)
    posts = Paginator(posts, 4)
    page_number = request.GET.get("page", 1)
    posts = posts.get_page(page_number)
    return render(
        request,
        "index.html",
        context={"posts": posts, "title": "Search for: " + search_query},
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you for your message! We will get back to you soon."
            )
            return redirect("blog:contact")
        else:
            if "captcha" in form.errors:
                messages.error(request, "Invalid CAPTCHA. Please try again.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = ContactForm()
    return render(
        request, "contactus.html", context={"title": "Contact Us", "form": form}
    )


def post_single(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="Published")
    comments = post.comments.all().order_by("-created_date")

    next_post = (
        Post.objects.filter(id__gt=post.id, status="Published").order_by("id").first()
    )
    prev_post = (
        Post.objects.filter(id__lt=post.id, status="Published").order_by("-id").first()
    )

    post.counted_views += 1
    post.save()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect("blog:post_detail", post_id=post.id)
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "next_post": next_post,
        "prev_post": prev_post,
    }

    return render(
        request,
        "blog-single.html",
        context=context,
    )


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("blog:index")
    else:
        form = PostForm()
    return render(
        request, "create_post.html", {"form": form, "title": "Create new post"}
    )
