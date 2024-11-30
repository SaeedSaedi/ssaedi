# urls.py
from django.urls import path
from blog.views import index, contact

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("contact-us", contact, name="contact"),
]
