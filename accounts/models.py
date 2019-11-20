from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='followings'
    )