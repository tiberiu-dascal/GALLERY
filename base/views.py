import datetime
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView

from .forms import AlbumForm, RegistrationForm
from .image_data import get_image_data
from .models import Album, Photo
from .utils.thumb_generator import generate_thumbs


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
def albums(request):
    albums = Album.objects.filter(owner=request.user.id)
    context = {"albums": albums}
    return render(request, "albums.html", context)


@login_required(login_url="login")
def photos(request):
    user = request.user
    countries = (
        Photo.objects.filter(album__owner_id=user.id).values("country").distinct()
    )
    streets = Photo.objects.filter(album__owner_id=user.id).values("street").distinct()
    cities = Photo.objects.filter(album__owner_id=user.id).values("city").distinct()
    albums = Photo.objects.filter(album__owner_id=user.id).values("album").distinct()

    def get_album_title(album):
        if Album.objects.get(id=album).title == "":
            return 0
        else:
            return Album.objects.get(id=album).title

    def get_titles(albums):
        titles = {}
        for album in albums:
            titles[album["album"]] = get_album_title(album["album"])
        return titles

    photos_obj = Photo.objects.filter(album__owner_id=user.id)

    if request.method == "POST":
        data = request.POST
        if data["country"] != "":
            photos_obj = photos_obj.filter(country=data["country"])
        if data["city"] != "":
            photos_obj = photos_obj.filter(city=data["city"])
        if data["street"] != "":
            photos_obj = photos_obj.filter(street=data["street"])
        if data["album"] != "":
            photos_obj = photos_obj.filter(album=data["album"])

    p = Paginator(photos_obj, 12)
    page = request.GET.get("page")
    photos = p.get_page(page)
    print(photos)
    context = {
        "photos": photos,
        "cities": cities,
        "countries": countries,
        "streets": streets,
        "albums": get_titles(albums),
    }

    return render(request, "photos.html", context)


@login_required(login_url="login")
def create_album(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect("/")
    form = AlbumForm()
    return render(request, "create_album.html", {"form": form})


class AlbumDeleteView(DeleteView):
    model = Album
    success_url = "/"
    template_name = "delete_album.html"


@login_required(login_url="login")
def edit_album(request, pk):
    user = request.user
    album = Album.objects.filter(pk=pk).get()
    if album.owner_id == user.id:
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")

            album.title = title
            album.description = description

            album.save(update_fields=["title", "description"])
            messages.success(request, "Album was updated successfully!")
            return redirect("/")
    else:
        messages.error(request, "Operation not Allowe!")
    context = {"album": album}
    return render(request, "edit_album.html", context)


@login_required(login_url="login")
def upload(request):
    user = request.user
    albums = Album.objects.filter(owner=user.id)
    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist("images")

        if images is not None:
            for image in images:
                photo = Photo.objects.create(
                    image=image,
                    album_id=data["album"],
                )
                photo.title = data["description"]
                try:
                    photo.save()
                    ps_photo = Photo.objects.latest("id")
                    generate_thumbs(ps_photo)
                    ps_photo.thumbnail = "thumbs/" + ps_photo.image.name
                    ps_photo_data = get_image_data(ps_photo.image.path)
                    if "error" in ps_photo_data:
                        ps_photo.save()
                        messages.warning(
                            request, "Image saved, but with limited information!"
                        )
                        # messages.error(ps_photo_data["error"])
                    else:
                        # get data and put it in the DB
                        ps_photo.date_taken = datetime.datetime.strptime(
                            ps_photo_data["date_taken"], "%Y-%m-%d %H:%M:%S"
                        )
                        ps_photo.make = ps_photo_data["make"]
                        ps_photo.model = ps_photo_data["model"]
                        ps_photo.orientation = ps_photo_data["orientation"]
                        ps_photo.x_resolution = ps_photo_data["x_resolution"]
                        ps_photo.y_resolution = ps_photo_data["y_resolution"]
                        ps_photo.resolution_unit = ps_photo_data["resolution_unit"]
                        ps_photo.latitude = ps_photo_data["latitude"]
                        ps_photo.longitude = ps_photo_data["longitude"]
                        ps_photo.country = ps_photo_data["country"]
                        ps_photo.county = ps_photo_data["county"]
                        ps_photo.zipcode = ps_photo_data["zipcode"]
                        ps_photo.city = ps_photo_data["city"]
                        ps_photo.street = ps_photo_data["street"]
                        ps_photo.save()
                except Exception:
                    messages.error(request, "Image could not be uploaded!")
                    return redirect("/")

            messages.success(request, "Photo(s) uploaded successfully!")
            return redirect("/")
        else:
            messages.error(request, "No images selected!")
            return redirect("/")
    context = {"albums": albums}
    return render(request, "upload.html", context)


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = "/"
    template_name = "confirm_delete.html"


def map_photos(request, pk):
    album = Album.objects.get(id=pk)
    photos = album.photo_set.all()
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
