import os
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".avi", ".mkv"}


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Qrcode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, default="Scan for Menu")
    file = models.FileField(upload_to='uploads/')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def media_type(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in VIDEO_EXTS:
            return "video"
        if ext in IMAGE_EXTS:
            return "image"
        return "other"