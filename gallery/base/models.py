from django.db import models


class User(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField()
    password = models.CharField(max_length=70)
    date = models.DateField(auto_now_add=True)
    albums = models.ManyToManyField("Album", related_name="albums")

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    photos = models.ManyToManyField("Photo", related_name="photos")

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=70)
    image = models.ImageField()
    date = models.DateField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    thumbnail = models.ImageField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
