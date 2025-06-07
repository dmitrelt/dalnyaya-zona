from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .forms import CommentForm, PostForm, ContactForm
from .models import Category, Post, Comment, PostLike, ContactMessage
from django.conf import settings
from .serializers import PostSerializer, CategorySerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views import View
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

class WelcomeView(TemplateView):
    template_name = 'forum/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yandex_maps_api_key'] = settings.YANDEX_MAPS_API_KEY
        context['form'] = ContactForm()
        context['form_success'] = self.request.session.pop('form_success', False)
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['form_success'] = True
            return redirect('welcome')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ForumHomeView(ListView):
    model = Category
    template_name = 'forum/index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Форум по настольному теннису'
        first_category = self.object_list.first()
        context['active_category'] = first_category
        if first_category:
            posts = first_category.posts.all()
            if self.request.user.is_authenticated:
                liked_post_ids = set(PostLike.objects.filter(
                    post__in=posts, user=self.request.user
                ).values_list('post_id', flat=True))
                context['posts'] = [
                    {
                        'post': post,
                        'user_liked': post.id in liked_post_ids,
                        'likes_count': post.likes.count()
                    }
                    for post in posts
                ]
            else:
                context['posts'] = [
                    {
                        'post': post,
                        'user_liked': False,
                        'likes_count': post.likes.count()
                    }
                    for post in posts
                ]
        else:
            context['posts'] = []
        return context

class CategoryPostsView(ListView):
    model = Post
    template_name = 'forum/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Форум - {self.category.title}'
        context['categories'] = Category.objects.all()
        context['active_category'] = self.category
        posts = self.get_queryset()
        if self.request.user.is_authenticated:
            liked_post_ids = set(PostLike.objects.filter(
                post__in=posts, user=self.request.user
            ).values_list('post_id', flat=True))
            context['posts'] = [
                {
                    'post': post,
                    'user_liked': post.id in liked_post_ids,
                    'likes_count': post.likes.count()
                }
                for post in posts
            ]
        else:
            context['posts'] = [
                {
                    'post': post,
                    'user_liked': False,
                    'likes_count': post.likes.count()
                }
                for post in posts
            ]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'forum/post-detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_object(self, queryset=None):
        category_slug = self.kwargs.get('category_slug')
        post_slug = self.kwargs.get('post_slug')
        return get_object_or_404(
            Post,
            category__slug=category_slug,
            slug=post_slug
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['categories'] = Category.objects.all()
        context['active_category'] = self.object.category
        comments = self.object.comments.filter(is_published=True)
        context['comments'] = [
            {'comment': comment} for comment in comments
        ]
        context['comment_form'] = CommentForm()
        if self.request.user.is_authenticated:
            context['user_liked_post'] = PostLike.objects.filter(post=self.object, user=self.request.user).exists()
        context['post_likes_count'] = self.object.likes.count()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post-create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('post_detail', kwargs={
            'category_slug': self.object.category.slug,
            'post_slug': self.object.slug
        })

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    login_url = '/users/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            Post,
            category__slug=self.kwargs['category_slug'],
            slug=self.kwargs['post_slug']
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={
            'category_slug': self.kwargs['category_slug'],
            'post_slug': self.kwargs['post_slug']
        }) + '#comments'

class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, category_slug, post_slug):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)

        post = get_object_or_404(Post, category__slug=category_slug, slug=post_slug)
        user = request.user
        try:
            liked = PostLike.objects.filter(post=post, user=user).exists()
            action = 'unliked' if liked else 'liked'

            if liked:
                PostLike.objects.filter(post=post, user=user).delete()
            else:
                PostLike.objects.create(post=post, user=user)

            likes_count = post.likes.count()
            logger.info(f"User {user.username} {action} post {post.id}, likes count: {likes_count}")

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'post_{post.id}',
                {
                    'type': 'like_update',
                    'message': {
                        'post_id': post.id,
                        'likes_count': likes_count,
                        'action': action,
                        'user_id': user.id
                    }
                }
            )

            return JsonResponse({
                'status': 'success',
                'action': action,
                'likes_count': likes_count
            })
        except Exception as e:
            logger.error(f"Error processing like for post {post.id} by user {user.username}: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)