# Generated by Django 5.1.7 on 2025-05-26 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_remove_comment_likes_remove_post_likes_commentlike_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentLike',
        ),
    ]
