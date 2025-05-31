from django.contrib import admin
from .models import Category, Post, Comment, PostLike, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('created_at',)
    ordering = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'is_published', 'created_at')
    list_editable = ('is_published',)
    ordering = ('-created_at',)
    actions = ['make_published', 'make_unpublished']

    @admin.action(description='Опубликовать выбранные посты')
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Снять с публикации выбранные посты')
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'is_published')
    search_fields = ('content', 'author__username')
    list_filter = ('post', 'is_published', 'created_at')
    list_editable = ('is_published',)
    ordering = ('-created_at',)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


