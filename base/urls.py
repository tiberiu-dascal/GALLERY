from django.urls import path

from . import views
from .views import PhotoDeleteView, AlbumDeleteView


urlpatterns = [
    path("", views.index, name="index"),
    path("create_album", views.create_album, name="create_album"),
    path("album/<pk>/", views.album, name="album"),
    path("albums", views.albums, name="albums"),
    path("upload", views.upload, name="upload"),
    path("<pk>/delete/", PhotoDeleteView.as_view()),
    path("<pk>/delete_album/", AlbumDeleteView.as_view()),
    path("map/<pk>/", views.map_photos, name="map"),
    path("photos", views.photos, name="photos"),
    path("register", views.register, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("profile/", views.edit_profile, name="profile"),
]
