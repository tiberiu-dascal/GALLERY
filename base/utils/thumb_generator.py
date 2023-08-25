import os
from PIL import Image, ImageOps


def generate_thumbs(img):
    try:
        image = Image.open(img.image.path)
        image.thumbnail((350, 350))
        image = ImageOps.exif_transpose(image)
        image.save(
            os.path.join(
                img.image.path.replace("/" + img.image.name, ""),
                "thumbs",
                img.image.name,
            )
        )
        print("Thumbnail created")
    except IOError as e:
        print("Cannot create thumbnail for", img.image.path, ": ", e)
