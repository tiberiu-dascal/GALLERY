from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Photo, Album


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ("title", "image", "album")


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
        widgets = {
            "username": widgets.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "first_name": widgets.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": widgets.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "email": widgets.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Password confirmation"


class EditProfileForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )
