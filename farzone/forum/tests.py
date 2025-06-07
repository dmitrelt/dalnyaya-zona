from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Post

User = get_user_model()

class ForumTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            slug='test-category'
        )

    def test_create_post(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            category=self.category,
            author=self.user
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author.username, 'testuser')
        self.assertEqual(post.category.title, 'Test Category')