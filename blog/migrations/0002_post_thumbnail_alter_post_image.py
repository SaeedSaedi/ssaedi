# Generated by Django 5.1.3 on 2024-11-30 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, default='posts/thumbnails/default.jpg', upload_to='posts/thumbnails/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='posts/default.jpg', upload_to='posts/'),
        ),
    ]
