# urls.py
from django.urls import path
from blog.views import under_development

urlpatterns = [
    path("", under_development, name="under_development"),
]
