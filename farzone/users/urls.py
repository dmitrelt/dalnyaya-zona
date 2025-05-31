from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.http import require_http_methods

from .views import RegisterView, ProfileView, ProfileEditView, PublicProfileView, AuthAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', PublicProfileView.as_view(), name='profile_view'),
    path('api/auth/', AuthAPIView.as_view(), name='api_auth'),
]