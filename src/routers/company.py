import json
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from starlette.responses import JSONResponse
from src.auth.auth import CustomUser, current_user
from src.db import get_async_session
from src.models import Company
from src.schemas.company import CompanyUpdate, CompanyRead
from src.utils import upload_image, PathSelector, get_image

router = APIRouter()


@router.get("/company/{uuid}", response_model=CompanyRead)
async def get_company(uuid: UUID, session: AsyncSession = Depends(get_async_session)):
    company = await session.get(Company, uuid)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company doesn't exist")
    del company.hashed_password
    if company.image:
        company.image = get_image(company.image)  # заменяем путь до картинки картинкой
    return company


@router.get("/company", response_model=List[CompanyRead])
async def get_companies(session: AsyncSession = Depends(get_async_session)):
    query = select(Company).options(load_only(Company.id, Company.inn, Company.email, Company.is_active, Company.is_verified, Company.is_superuser, Company.company_name, Company.description, Company.field_of_activity, Company.year_of_foundation, Company.city, Company.street, Company.house, Company.number_of_employees, Company.image, Company.personal_site, Company.phone, Company.contact_email, Company.social_network_link, Company.registered_at))
    companies = await session.execute(query)
    return companies.scalars().all()


@router.put("/company", response_model=dict)
async def update_company(cmp: CompanyUpdate, session: AsyncSession = Depends(get_async_session),
                         user: CustomUser = Depends(current_user)):
    company = await session.get(Company, user.id)
    for key, val in cmp:
        if val and key != 'file':
            setattr(company, key, val)
    try:
        image_url = None
        if cmp.file:
            image_url = await upload_image(cmp.file, PathSelector.company)
    except Exception as ex:
        return HTTPException(status_code=400, detail=str(ex))

    company.image = image_url
    await session.commit()
    return JSONResponse(content={'message': 'Updated successfully'}, status_code=200)
