from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Photo, Album
from .forms import PhotoForm, AlbumForm, RegistrationForm
from .get_coords import get_image_coordinates


# Create your views here.
def index(request):
    photos = Photo.objects.all()
    context = {"photos": photos}
    return render(request, "index.html", context)


def album(request, pk):
    album = Album.objects.get(id=pk)
    photos = album.photo_set.all()
    context = {"photos": photos, "album": album}
    return render(request, "album.html", context)


def create_album(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    form = AlbumForm()
    return render(request, "create_album.html", {"form": form})


def upload(request):
    # TODO: add latitude and longitude to photo object before saving
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo uploaded successfully")
            return redirect("/")
    form = PhotoForm()
    return render(request, "upload.html", {"form": form})


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = "/"
    template_name = "confirm_delete.html"


def map_photos(request, pk):
    album = Album.objects.get(id=pk)
    photos = album.photo_set.all()
    for photo in photos:
        # we need to add the latitude and longitude from the image
        # and add it to the photo object
        if photo.latitude is None or photo.longitude is None:
            photo.latitude = get_image_coordinates(photo.image.path)[0]
            photo.longitude = get_image_coordinates(photo.image.path)[1]

    context = {"photos": photos, "album": album}
    return render(request, "map_photos.html", context)


def register(request):
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account created successfully for " + user)
            return redirect("/")
        else:
            messages.error(request, "Error creating account" + str(form._errors))
            return redirect("register")

    context = {"form": form}
    return render(request, "register.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login user
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("/")
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect("login")
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("/")
