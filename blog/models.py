import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.conf import settings


# Create your models here.
@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        if instance.pk:
            filename = "{}.{}".format(instance.pk, ext)
        else:
            filename = "{}.{}".format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    counted_views = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(
        upload_to=UploadToPathAndRename("posts/"), default="posts/default.jpg"
    )
    thumbnail = models.ImageField(
        upload_to=UploadToPathAndRename("posts/thumbnails/"),
        default="posts/thumbnails/default.jpg",
    )
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.id})


class Newsletter(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
