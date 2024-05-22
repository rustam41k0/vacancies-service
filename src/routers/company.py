from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from starlette.responses import JSONResponse
from src.auth.auth import CustomUser, current_user
from src.db import get_async_session
from src.models import Company
from src.schemas.company import CompanyUpdate, CompanyRead
from src.utils import upload_image_to_s3_and_save_url_to_db, delete_image_from_s3_and_from_db

router = APIRouter()


@router.get("/company/{uuid}", response_model=CompanyRead)
async def get_company(uuid: UUID, session: AsyncSession = Depends(get_async_session)):
    company = await session.get(Company, uuid)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company doesn't exist")
    del company.hashed_password
    return company


@router.get("/company", response_model=List[CompanyRead])
async def get_companies(session: AsyncSession = Depends(get_async_session)):
    query = select(Company).options(
        load_only(Company.id, Company.inn, Company.email, Company.is_active, Company.is_verified, Company.is_superuser,
                  Company.company_name, Company.description, Company.field_of_activity, Company.year_of_foundation,
                  Company.city, Company.street, Company.house, Company.number_of_employees, Company.image_id,
                  Company.personal_site, Company.phone, Company.contact_email, Company.social_network_link,
                  Company.registered_at))
    companies = await session.execute(query)
    return companies.scalars().all()


@router.put("/company")
async def update_company(cmp: CompanyUpdate,
                         session: AsyncSession = Depends(get_async_session),
                         user: CustomUser = Depends(current_user)):
    company = await session.get(Company, user.id)
    for key, val in cmp:
        setattr(company, key, val)
    await session.commit()
    return JSONResponse(content={'message': 'Updated successfully'}, status_code=200)


@router.put("/company/image")
async def upload_company_image(file: UploadFile,
                               session: AsyncSession = Depends(get_async_session),
                               user: CustomUser = Depends(current_user)):
    company = await session.get(Company, user.id)
    try:
        image_uuid = await upload_image_to_s3_and_save_url_to_db(file, session)
        company.image_id = image_uuid
        await session.commit()
        return JSONResponse(content={'message': 'Updated successfully'}, status_code=200)
    except Exception as ex:
        return HTTPException(status_code=500, detail=str(ex))


@router.delete("/company/image")
async def delete_company_image(session: AsyncSession = Depends(get_async_session),
                               user: CustomUser = Depends(current_user)):
    company = await session.get(Company, user.id)
    if company.image_id:
        await delete_image_from_s3_and_from_db(company.image_id, session)
        company.image_id = None
        await session.commit()
        return JSONResponse(content={'message': 'Deleted successfully'}, status_code=200)
    else:
        return HTTPException(status_code=400, detail="Company image doesn't exist")
