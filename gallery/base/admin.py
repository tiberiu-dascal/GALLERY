from django.contrib import admin
from .models import User, Album, Photo

# Register your models here.
admin.site.register(User)
admin.site.register(Album)
admin.site.register(Photo)
