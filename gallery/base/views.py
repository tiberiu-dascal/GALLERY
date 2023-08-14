from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Photo, User, Album
from .forms import PhotoForm, AlbumForm
from .get_coords import get_image_coordinates

# from django.contrib import messages # will be used later


# Create your views here.
def index(request):
    albums = Album.objects.all()
    context = {"albums": albums}
    return render(request, "index.html", context)


@login_required
def album(request, pk):
    if user.is_authenticated:
        album = Album.objects.get(id=pk)
        photos = album.photo_set.all()
        context = {"photos": photos, "album": album}
        return render(request, "album.html", context)
    else:
        return render(request, "login.html")


@login_required
def create_album(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    form = AlbumForm()
    return render(request, "create_album.html", {"form": form})


@login_required
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
        # check if user exists
        # if user exists, redirect to login page
        # if user does not exist, create user and redirect to index page
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(name=name, email=email, password=password)
            return redirect("login")
        except User.DoesNotExist:
            user = User.objects.create(name=name, email=email, password=password)
            request.session["user_id"] = user.id
            return redirect("/")
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("user logedin")
            return redirect("home")
        else:
            return render(request, "login.html", {"invalid": "invalid credentials"})
    else:
        return render(request, "login.html")


@login_required
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
