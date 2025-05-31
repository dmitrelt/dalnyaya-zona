from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.id}/{filename}'


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(
        _('avatar'),
        upload_to=user_avatar_path,
        blank=True,
        null=True
    )
    blade = models.CharField(_('blade'), max_length=100, blank=True)
    rubber_fh = models.CharField(_('forehand rubber'), max_length=100, blank=True)
    rubber_bh = models.CharField(_('backhand rubber'), max_length=100, blank=True)
    bio = models.TextField(_('bio'), blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username
