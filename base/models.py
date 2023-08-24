from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=70, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=70, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Album(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=70)
    image = models.ImageField()
    date = models.DateField(auto_now_add=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
