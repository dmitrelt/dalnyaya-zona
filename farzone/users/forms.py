from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )


class ProfileEditForm(UserChangeForm):
    password = None  # Убираем поле смены пароля

    class Meta:
        model = User
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'email',
            'bio',
            'blade',
            'rubber_fh',
            'rubber_bh'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
