from django import forms
from .models import Photo, User, Album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("title", "image", "album")


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("title", "description")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email", "password")
