import datetime
from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .utils.thumb_generator import generate_thumbs
from .models import Photo, Album
from .forms import PhotoForm, AlbumForm, RegistrationForm, EditProfileForm
from .get_coords import get_image_coordinates


# Create your views here.
def index(request):
    year = datetime.datetime.now().year
    if request.user.is_authenticated:
        user = request.user
        albums = Album.objects.filter(owner=user.id)
        photos = Photo.objects.filter(album__in=albums)

        context = {"albums": albums, "photos": photos, "year": year}
        return render(request, "index.html", context)
    return render(request, "index.html", {"year": year})


@login_required(login_url="login")
def album(request, pk):
    album = Album.objects.get(id=pk)
    photos = album.photo_set.all()
    context = {"photos": photos, "album": album}
    return render(request, "album.html", context)


@login_required(login_url="login")
def create_album(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    form = AlbumForm()
    return render(request, "create_album.html", {"form": form})


@login_required(login_url="login")
def upload(request):
    # TODO: add latitude and longitude to photo object before saving
    user = request.user
    albums = Album.objects.filter(owner=user.id)
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            photo = Photo.objects.latest("id")
            generate_thumbs(photo)
            photo.thumbnail.name = "thumbs/" + photo.image.name
            photo.latitude = get_image_coordinates(photo.image.path)[0]
            photo.longitude = get_image_coordinates(photo.image.path)[1]
            photo.save()

            messages.success(request, "Photo uploaded successfully")
            return redirect("/")
        else:
            messages.error(request, "Error uploading photo" + str(form._errors))
            return redirect("upload")
    form = PhotoForm()
    context = {"albums": albums, "form": form}
    return render(request, "upload.html", context)


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


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("/")


@login_required(login_url="login")
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save(update_fields=["username", "first_name", "last_name"])
        messages.success(request, "Profile updated successfully")
        return redirect("/")
        # else:
        # messages.error(request, "Error updating profile")
        # return redirect("profile")
        # form = EditProfileForm(request.POST, instance=user)
        # if form.is_valid():
        #     form.save(update_fields=["first_name", "last_name"])
        #     messages.success(request, "Profile updated successfully")
        #     return redirect("/")
        # else:
        #     messages.error(request, "Error updating profile" + str(form._errors))
        #     return redirect("profile")
    context = {"user": user}
    return render(request, "edit_profile.html", context)


def reset_password(request, user):
    pass
