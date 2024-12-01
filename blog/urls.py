# urls.py
from django.urls import path
from blog.views import index, contact, post_single

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("posts/<int:post_id>/", post_single, name="post_detail"),
    path("contact-us", contact, name="contact"),
]
