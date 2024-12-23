# Generated by Django 5.1.3 on 2024-11-30 14:32

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_post_thumbnail_alter_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                default="posts/default.jpg",
                upload_to=blog.models.UploadToPathAndRename("posts/"),
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="thumbnail",
            field=models.ImageField(
                default="posts/thumbnails/default.jpg",
                upload_to=blog.models.UploadToPathAndRename("posts/thumbnails/"),
            ),
        ),
    ]
