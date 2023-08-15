from django.db import models


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
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
