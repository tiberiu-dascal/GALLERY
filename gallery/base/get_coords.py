from exif import Image

# from geopy.geocoders import Nominatim


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def get_image_coordinates(image_path):
    with open(image_path, "rb") as src:
        img = Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (
                decimal_coords(img.gps_latitude, img.gps_latitude_ref),
                decimal_coords(img.gps_longitude, img.gps_longitude_ref),
            )
        except AttributeError:
            print("No Coordinates")
    else:
        coords = (0, 0)
        print("The Image has no EXIF information")

    return [coords[0], coords[1]]


# c = image_coordinates(sys.argv[1])

# Initialize Nominatim API
# geolocator = Nominatim(user_agent="geoapiExercises")


# Get location with geocode
# location = geolocator.geocode(str(c[0]) + "," + str(c[1]))
#
# # Display location
# print("\nLocation of the given Latitude and Longitude:")
# print(location)
