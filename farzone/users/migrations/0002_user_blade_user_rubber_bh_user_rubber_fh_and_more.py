# Generated by Django 5.1.7 on 2025-05-14 01:06

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blade',
            field=models.CharField(blank=True, max_length=100, verbose_name='blade'),
        ),
        migrations.AddField(
            model_name='user',
            name='rubber_bh',
            field=models.CharField(blank=True, max_length=100, verbose_name='backhand rubber'),
        ),
        migrations.AddField(
            model_name='user',
            name='rubber_fh',
            field=models.CharField(blank=True, max_length=100, verbose_name='forehand rubber'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.user_avatar_path, verbose_name='avatar'),
        ),
    ]
