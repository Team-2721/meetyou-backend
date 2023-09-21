from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from core.utils import upload_to


class User(AbstractUser):
    nickname = models.CharField(max_length=20, verbose_name="닉네임")
    avatar = models.ImageField(
        upload_to=upload_to("avatars", True), blank=True, verbose_name="프로필 사진"
    )
