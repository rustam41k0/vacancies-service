from typing import List, Union
from uuid import UUID
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import current_user
from src.db import get_async_session
from src.models import Image, CustomUser
from src.schemas.photo import ImageRead
from src.utils import delete_image_from_s3_and_from_db, upload_image_to_s3_and_save_url_to_db, get_company_image

router = APIRouter()

get_all_photo_description = 'Отдает все фотографии за исключением фотографий компаний'
delete_photo_description = 'Если указать is_company_photo=True и при этом указать uuid, то он попытается удалить ' \
                           'фотографию у компании, а не по uuid '


@router.post("/photo")
async def upload_photo_or_upload_company_photo(file: UploadFile,
                                               is_company_photo: bool = False,
                                               session: AsyncSession = Depends(get_async_session),
                                               user: CustomUser = Depends(current_user)):
    try:
        company_id = user.id if is_company_photo else None
        await upload_image_to_s3_and_save_url_to_db(file, session, company_id)
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


@router.get("/photo",
            response_model=List[ImageRead],
            description=get_all_photo_description)
async def get_all_photos(session: AsyncSession = Depends(get_async_session)):
    query = select(Image).filter(Image.company_id == None)
    images = await session.execute(query)
    return images.scalars().all()


@router.delete("/photo", description=delete_photo_description)
async def delete_photo_or_delete_company_photo(uuid: UUID = None,
                                               user: CustomUser = Depends(current_user),
                                               is_company_photo: bool = False,
                                               session: AsyncSession = Depends(get_async_session)):
    if not uuid and not is_company_photo:
        return HTTPException(status_code=400, detail="You haven't specified what needs to be removed")

    if is_company_photo:
        company_image = await get_company_image(user.id, session)
        if not company_image:
            return HTTPException(status_code=400, detail="Company doesn't have the photo")
        await delete_image_from_s3_and_from_db(company_image.id, session)
    else:
        is_deleted = await delete_image_from_s3_and_from_db(uuid, session)
        if not is_deleted:
            return HTTPException(status_code=400, detail="Photo doesn't exist")
    return JSONResponse(content={"message": f"Photo deleted successfully"}, status_code=200)
