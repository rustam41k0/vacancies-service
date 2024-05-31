from typing import List
from sqlalchemy import text
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from src.auth.auth import CustomUser, current_user
from src.db import get_async_session
from src.models import Company
from src.schemas.company import CompanyUpdate, CompanyRead
from src.utils import get_company_image

router = APIRouter()


@router.get("/company/{uuid}", response_model=CompanyRead)
async def get_company(uuid: UUID, session: AsyncSession = Depends(get_async_session)):
    company = await session.get(Company, uuid)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company doesn't exist")

    company.image_id = None
    company.image_url = None
    image = await get_company_image(uuid, session)
    if image:
        company.image_id = image.id
        company.image_url = image.image_url
    return company


@router.get("/company", response_model=List[CompanyRead])
async def get_companies(session: AsyncSession = Depends(get_async_session)):
    query = text(
        'SELECT c.id, c.inn, c.email, c.is_active, c.is_superuser, c.is_verified, c.company_name, '
        'c.description, c.field_of_activity, c.year_of_foundation, c.city, c.street, c.house, '
        'c.number_of_employees, c.personal_site, c.phone, c.contact_email, c.social_network_link, '
        'c.registered_at, i.id AS image_id, i.image_url FROM company AS c LEFT JOIN image AS i ON i.company_id = c.id;'
    )
    companies = await session.execute(query)
    return companies.mappings().all()


@router.put("/company")
async def update_company(cmp: CompanyUpdate,
                         session: AsyncSession = Depends(get_async_session),
                         user: CustomUser = Depends(current_user)):
    company = await session.get(Company, user.id)
    for key, val in cmp:
        setattr(company, key, val)
    await session.commit()
    return JSONResponse(content={'message': 'Updated successfully'}, status_code=200)
