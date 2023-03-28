from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(name='username', max_length=40, unique=True)
    email = models.EmailField(name='email')
    image_url = models.ImageField(name='image_url', null=True, blank=True, upload_to="user_profile_photos/%Y/%m/%d/")
    date_joined = models.DateTimeField(name='date_joined', auto_now_add=True)
    is_active = models.BooleanField(name='is_active', default=False)
    is_staff = models.BooleanField(name='is_staff', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        unique_together = ('username', 'email',)


class Follow(models.Model):
    user_is_following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    user_is_being_followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_friends = models.BooleanField(blank=True, default=False)
