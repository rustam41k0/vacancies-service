import os
from enum import Enum

from fastapi import UploadFile
from starlette.responses import FileResponse


class PathSelector(Enum):
    company = '../media/company/'
    photo = '../media/photo/'


async def upload_image(file: UploadFile, place: PathSelector):
    image_name = file.filename
    os.makedirs(str(place.value), exist_ok=True)
    image_path = place.value + image_name
    check_valid_extension(image_name)
    check_image_exists(image_path, image_name)
    contents = await file.read()
    with open(image_path, "wb") as f:
        f.write(contents)
    return image_path


def check_image_exists(photo_path: str, image_name: str):
    if os.path.exists(photo_path):
        raise Exception(f"File with name {image_name} already exists, rename your image")


def check_valid_extension(image_name: str):
    image_extensions = (".jpg", ".jpeg", ".png")
    if not image_name.lower().endswith(image_extensions):
        raise Exception("Invalid image format")


def get_image(image_path: str) -> FileResponse:
    if os.path.exists(image_path):
        return FileResponse(image_path)
    raise Exception("Image doesn't exist, invalid path")
