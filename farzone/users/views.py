from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView
from rest_framework.views import APIView

from forum.models import Post
from .forms import RegisterForm, LoginForm, ProfileEditForm
from .models import User

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class AuthAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('forum_home')
        return render(request, 'users/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('forum_home')
        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('forum_home')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.object)
        context['is_own_profile'] = True  # Указываем, что это профиль текущего пользователя
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/profile_edit.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')


class PublicProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.object)
        context['is_own_profile'] = (self.request.user == self.object)
        return context