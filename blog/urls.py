# urls.py
from django.urls import path
from blog.views import index, contact, post_single, blog_search, create_post

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("posts/<int:post_id>/", post_single, name="post_detail"),
    path("posts/create_new/", create_post, name="create_new_post"),
    path("search/", blog_search, name="search"),
    path("contact-us", contact, name="contact"),
]
