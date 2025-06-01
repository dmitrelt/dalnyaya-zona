from django.urls import path
from .views import (
    ForumHomeView,
    CategoryPostsView,
    PostDetailView,
    PostCreateView,
    CommentCreateView,
    WelcomeView,
    PostListCreateAPIView,
    CategoryListAPIView,
    PostLikeView,
)

app_name = 'forum'

urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('forum/', ForumHomeView.as_view(), name='forum_home'),
    path('category/<slug:slug>/', CategoryPostsView.as_view(), name='category_posts'),
    path('category/<slug:slug>/new/', PostCreateView.as_view(), name='post_create'),
    path('category/<slug:category_slug>/<slug:post_slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/<slug:post_slug>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('category/<slug:category_slug>/<slug:post_slug>/like/', PostLikeView.as_view(), name='post_like'),
    path('api/posts/', PostListCreateAPIView.as_view(), name='post_list_create_api'),
    path('api/categories/', CategoryListAPIView.as_view(), name='category_list_api'),
]