from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from src.custom_types import EmploymentEnum, ExperienceEnum


class VacancyRead(BaseModel):
    id: UUID
    name: str
    salary: int
    description: str
    city: str
    employment: EmploymentEnum
    experience: ExperienceEnum
    company_id: UUID


class VacancyCreate(BaseModel):
    name: str
    salary: int
    description: str
    city: str
    employment: EmploymentEnum
    experience: ExperienceEnum


class VacancyUpdate(BaseModel):
    name: Optional[str] = None
    salary: Optional[int] = None
    description: Optional[str] = None
    city: Optional[str] = None
    employment: Optional[EmploymentEnum] = None
    experience: Optional[ExperienceEnum] = None
