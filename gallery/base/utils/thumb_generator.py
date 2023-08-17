import os
from PIL import Image, ImageOps


def generate_thumbs(img):
    try:
        image = Image.open(img.path)
        image.thumbnail((350, 350))
        image = ImageOps.exif_transpose(image)
        image.save(os.path.join(img.path, "thumbs", img))
    except IOError:
        pass
