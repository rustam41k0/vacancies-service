from typing import List, Union
from uuid import UUID
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_async_session
from src.models import Image
from src.schemas.photo import ImageRead
from src.utils import delete_image_from_s3_and_from_db, upload_image_to_s3_and_save_url_to_db

router = APIRouter()


@router.post("/photo")
async def upload_photo(file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    try:
        await upload_image_to_s3_and_save_url_to_db(file, session)
        return JSONResponse(
            content={"message": "Image uploaded successfully", "filename": f"{file.filename}"},
            status_code=200
        )
    except Exception as ex:
        return HTTPException(status_code=500, detail=str(ex))


@router.get("/photo/{uuid}", response_model=Union[ImageRead, None])
async def get_photo(uuid: UUID, session: AsyncSession = Depends(get_async_session)):
    image = await session.get(Image, uuid)
    return image


@router.get("/photo", response_model=List[ImageRead])
async def get_all_photos(session: AsyncSession = Depends(get_async_session)):
    query = select(Image)
    images = await session.execute(query)
    return images.scalars().all()


@router.delete("/photo")
async def delete_photo(uuid: UUID, session: AsyncSession = Depends(get_async_session)):
    await delete_image_from_s3_and_from_db(uuid, session)
    image = await session.get(Image, uuid)
    await session.delete(image)
    await session.commit()
    return JSONResponse(content={"message": f"Photo {image.name} deleted successfully"}, status_code=200)
