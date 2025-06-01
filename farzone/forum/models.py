import itertools
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid
import requests
import logging

logger = logging.getLogger(__name__)

class Category(models.Model):
    title = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = str(uuid.uuid4().hex[:8])
            else:
                max_length = self._meta.get_field('slug').max_length
                if len(base_slug) > max_length - 6:
                    base_slug = base_slug[:max_length - 6]
            self.slug = base_slug
            for i in itertools.count(1):
                if not Category.objects.filter(slug=self.slug).exists():
                    break
                suffix = str(uuid.uuid4().hex[:4])
                self.slug = f"{base_slug}-{suffix}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'slug': self.slug})

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name='posts',
        verbose_name='Автор'
    )
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField('Содержание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='Категория')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = str(uuid.uuid4().hex[:8])
            else:
                max_length = self._meta.get_field('slug').max_length
                if len(base_slug) > max_length - 6:
                    base_slug = base_slug[:max_length - 6]
            self.slug = base_slug
            for i in itertools.count(1):
                if not Post.objects.filter(slug=self.slug).exists():
                    break
                suffix = str(uuid.uuid4().hex[:4])
                self.slug = f"{base_slug}-{suffix}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'category_slug': self.category.slug, 'post_slug': self.slug})

class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('Комментарий')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f'Комментарий от {self.author.username} к посту "{self.post.title}"'

class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_likes',
        verbose_name='Пользователь'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Пост'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк поста'
        verbose_name_plural = 'Лайки постов'
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user', 'post']),
        ]

    def __str__(self):
        return f'Лайк от {self.user.username} на пост "{self.post.title}"'

class ContactMessage(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = 'Сообщения обратной связи'
        ordering = ['-created_at']

    def __str__(self):
        return f'Сообщение от {self.name} ({self.email})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.is_notified:
            try:
                response = requests.post(
                    f"{settings.NOTIFIER_URL.rstrip('/')}/notifications/",
                    headers={
                        'X-API-Key': settings.NOTIFIER_API_KEY,
                        'Content-Type': 'application/json',
                    },
                    json={
                        'name': self.name,
                        'email': self.email,
                        'message': self.message,
                    },
                    timeout=5,
                )
                response.raise_for_status()
                self.is_notified = True
                super().save(update_fields=['is_notified'])
            except requests.RequestException as e:
                logger.error(f"Failed to send notification to Telegram: {str(e)}")