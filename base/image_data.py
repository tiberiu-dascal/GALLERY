from exif import Image
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="gallery_app")


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
        exifdata = img.list_all()
        # print(exifdata)
        for k, v in exifdata.items():
            print(k, v)
        try:
            date_taken = img.datetime_original
            date = date_taken.split(" ")[0]
            time = date_taken.split(" ")[1]
            date_taken = date.replace(":", "-") + " " + time
            make = img.make
            model = img.model
            orientation = img.orientation
            x_resolution = img.x_resolution
            y_resolution = img.y_resolution
            resolution_unit = img.resolution_unit
            latitude = decimal_coords(img.gps_latitude, img.gps_latitude_ref)
            longitude = decimal_coords(img.gps_longitude, img.gps_longitude_ref)

            location = geolocator.reverse(str(latitude) + "," + str(longitude))
            address = location.raw["address"]

            country = address.get("country", "")
            county = address.get("county", "")
            zipcode = address.get("postcode", "")
            city = address.get("city", "")
            street = address.get("road", "")

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
                "county": county,
                "zipcode": zipcode,
                "city": city,
                "street": street,
            }
        except AttributeError:
            return {"error": "Missing attributes"}
    else:
        return {"error": "Image has no exif data"}
