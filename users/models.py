from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse


class User(AbstractUser):
    nickname = models.CharField(max_length=20)
