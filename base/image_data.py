from exif import Image

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geoapiExercise")


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def get_image_data(image):
    # get all data from exif
    with open(image, "rb") as src:
        img = Image(src)
    if img.has_exif:
        try:
            # Sample data that needs to be returned by the function

            # date_taken = models.DateField(blank=True, null=True)
            # make = models.CharField(max_length=70, blank=True, null=True)
            # model = models.CharField(max_length=70, blank=True, null=True)
            # orientation = models.CharField(max_length=70, blank=True, null=True)
            # x_resolution = models.FloatField(blank=True, null=True)
            # y_resolution = models.FloatField(blank=True, null=True)
            # resolution_unit = models.CharField(max_length=70, blank=True, null=True)
            # date_uploaded = models.DateField(auto_now_add=True)
            # latitude = models.FloatField(blank=True, null=True)
            # longitude = models.FloatField(blank=True, null=True)
            # country = models.CharField(max_length=70, blank=True, null=True)
            # city = models.CharField(max_length=70, blank=True, null=True)
            # street = models.CharField(max_length=70, blank=True, null=True)

            date_taken = img.datetime_original
            make = img.make
            model = img.model
            orientation = img.orientation
            x_resolution = img.x_resolution
            y_resolution = img.y_resolution
            resolution_unit = img.resolution_unit
            latitude = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
            longitude = decimal_coords(img.gps_logitude, img.gps_longitude_ref)
            country = None
            city = None
            street = None
            location = geolocator.geocode(str(latitude) + "," + str(longitude))

            return {
                "date_taken": date_taken,
                "make": make,
                "model": model,
                "orientation": orientation,
                "x_resolution": x_resolution,
                "y_resolution": y_resolution,
                "resolution_unit": resolution_unit,
                "latitude": latitude,
                "longitude": longitude,
                "country": country,
                "city": city,
                "street": street,
            }
        except AttributeError:
            return {"error": "No exif data found"}


def get_image_coordinates(image_path):
    with open(image_path, "rb") as src:
        img = Image(src)
    coords = (0, 0)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (
                decimal_coords(img.gps_latitude, img.gps_latitude_ref),
                decimal_coords(img.gps_longitude, img.gps_longitude_ref),
            )
        except AttributeError:
            print("No Coordinates")

    return [coords[0], coords[1]]


# c = get_image_coordinates(sys.argv[1])

# Initialize Nominatim API


# Get location with geocode
# location = geolocator.geocode(str(c[0]) + "," + str(c[1]))
#
# # Display location
# print("\nLocation of the given Latitude and Longitude:")
# print(location)
