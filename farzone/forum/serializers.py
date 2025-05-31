from rest_framework import serializers
from .models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at', 'likes_count']
        read_only_fields = ['id', 'author', 'created_at', 'post']

    def get_likes_count(self, obj):
        return obj.likes.count()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'category', 'created_at', 'likes_count']
        read_only_fields = ['id', 'slug', 'author', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()
