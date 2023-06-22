from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from PIL import Image


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="Profile Pictures/")

    def __str__(self) -> str:
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 50)
            img.thumbnail(output_size)
            img.save(self.image.path)
