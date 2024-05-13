from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from src.custom_types import SalaryEnum, EmploymentEnum, ExperienceEnum
from src.auth.auth import current_user, CustomUser
from src.db import get_async_session
from src.models import Vacancy
from src.schemas.vacancy import VacancyRead, VacancyCreate, VacancyUpdate

router = APIRouter()


async def access_check(uuid: UUID, user_id: str, session: AsyncSession):
    vacancy = await session.get(Vacancy, uuid)
    if not vacancy or vacancy.company_id != user_id:
        raise HTTPException(status_code=404, detail=f"Vacancy doesn't exist")
    return True


@router.get("/vacancy", response_model=List[VacancyRead])
async def get_vacancies(salary: Optional[SalaryEnum] = None,
                        name: Optional[str] = None,
                        city: Optional[str] = None,
                        employment: Optional[EmploymentEnum] = None,
                        experience: Optional[ExperienceEnum] = None,
                        company_id: Optional[UUID] = None,
                        session: AsyncSession = Depends(get_async_session)):
    query = select(Vacancy)
    if name:
        query = query.filter(Vacancy.name == name)
    if city:
        query = query.filter(Vacancy.city == city)
    if employment:
        query = query.filter(Vacancy.employment == employment)
    if experience:
        query = query.filter(Vacancy.experience == experience)
    if company_id:
        query = query.filter(Vacancy.company_id == company_id)
    if salary:
        query = query.order_by(Vacancy.salary) if salary == salary.asc else query.order_by(desc(Vacancy.salary))
    vacancies = await session.execute(query)
    return vacancies.scalars().all()


@router.get("/vacancy/{uuid}", response_model=VacancyRead)
async def get_vacancy(uuid: UUID, session: AsyncSession = Depends(get_async_session)):
    vacancy = await session.get(Vacancy, uuid)
    if not vacancy:
        raise HTTPException(status_code=404, detail=f"Vacancy doesn't exist")
    return vacancy


@router.post("/vacancy", response_model=dict)
async def create_vacancy(vac: VacancyCreate, session: AsyncSession = Depends(get_async_session),
                         user: CustomUser = Depends(current_user)):
    vacancy = Vacancy(
        name=vac.name,
        salary=vac.salary,
        description=vac.description,
        city=vac.city,
        employment=vac.employment,
        experience=vac.experience,
        company_id=user.id
    )
    session.add(vacancy)
    await session.commit()
    return JSONResponse(content={"message": f"Vacancy created successfully"}, status_code=200)


@router.put("/vacancy/{uuid}", response_model=dict)
async def update_vacancy(uuid: UUID, vac: VacancyUpdate, session: AsyncSession = Depends(get_async_session),
                         user: CustomUser = Depends(current_user)):
    await access_check(uuid, user.id, session)

    vacancy = await session.get(Vacancy, uuid)
    for key, val in vac:
        if val:
            setattr(vacancy, key, val)
    await session.commit()
    return JSONResponse(content={"message": f"Vacancy updated successfully"}, status_code=200)


@router.delete("/vacancy/{uuid}", response_model=dict)
async def delete_vacancy(uuid: UUID, session: AsyncSession = Depends(get_async_session),
                         user: CustomUser = Depends(current_user)):
    await access_check(uuid, user.id, session)
    vacancy = await session.get(Vacancy, uuid)

    await session.delete(vacancy)
    await session.commit()
    return JSONResponse(content={"message": f"Vacancy deleted successfully"}, status_code=200)
