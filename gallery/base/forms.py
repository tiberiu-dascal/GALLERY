from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Photo, Album


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ("title", "image")


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ("title", "description")


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
