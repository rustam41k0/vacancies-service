import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from src.utils import upload_image, PathSelector, get_image

router = APIRouter()


@router.post("/photo")
async def upload_photo(file: UploadFile):
    try:
        await upload_image(file, PathSelector.photo)
        return JSONResponse(
            content={"message": "Image uploaded successfully", "filename": f"{file.filename}"},
            status_code=200
        )
    except Exception as ex:
        return HTTPException(status_code=400, detail=str(ex))


@router.get("/photo")  # TODO: в нужном ли формате выдаются картинки?
async def get_all_photos():
    media_dir = str(PathSelector.photo.value)
    photo_names = []
    if os.path.exists(media_dir):
        photo_names = [file.name for file in Path(media_dir).iterdir() if file.is_file()]
    photos = []

    for photo_name in photo_names:
        image = get_image(media_dir + photo_name)
        photos.append(image)
    return {"photos": photos}


@router.delete("/photo")
async def delete_photo(photo_name: str):
    photo_path = str(PathSelector.photo.value) + photo_name
    if os.path.exists(photo_path):
        os.remove(photo_path)
        return JSONResponse(content={"message": f"Photo {photo_name} deleted successfully"}, status_code=200)
    else:
        return HTTPException(status_code=400, detail=f"Photo with name {photo_name} doesn't exist")
