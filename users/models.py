from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg")
    bio = models.TextField(null=True, blank=True, verbose_name="Biografia")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Data urodzenia")
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numer telefonu")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil {self.user.username}"
