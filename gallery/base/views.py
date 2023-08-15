from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Photo, User, Album
from .forms import PhotoForm, AlbumForm
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
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    form = PhotoForm()
    return render(request, "upload.html", {"form": form})


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = "/"
    template_name = "confirm_delete.html"


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password_confirm"]

        if (
            name == ""
            or email == ""
            or password == ""
            or password2 == ""
            or password != password2
        ):
            messages.warning(request, "Please fill in all the fields")
            return redirect("register")

        if User.objects.filter(name=name).exists():
            messages.error(request, "Username is already taken")
            return redirect("register")
        else:
            user = User.objects.create(name=name, email=email, password=password)
            user.save()
            messages.success(request, "You are now registered")
            return redirect("index")
    return render(request, "register.html")


@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "You are now logged out")
    return redirect("index")


def login_user(request):
    if request.method == "POST":
        user = request.POST["user"]
        password = request.POST["password"]
        if User.objects.filter(name=user).exists():
            user = auth.authenticate(user=user, password=password)

        if user is not None:
            login(request, user)
            print("user logged in")
            messages.success(request, "You are now logged in")
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "login.html")
    else:
        return render(request, "login.html")


def map_photos(request, pk):
    album = Album.objects.get(id=pk)
    photos = album.photo_set.all()
    for photo in photos:
        # we need to add the latitude and longitude from the image
        # and add it to the photo object
        photo.latitude = get_image_coordinates(photo.image.path)[0]
        photo.longitude = get_image_coordinates(photo.image.path)[1]

    context = {"photos": photos, "album": album}
    return render(request, "map_photos.html", context)
