from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi_users import schemas
from pydantic import BaseModel
from src.schemas.photo import ImageRead


class CompanyReadAuth(schemas.BaseUser):
    id: UUID
    inn: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    company_name: Optional[str]
    description: Optional[str]
    field_of_activity: Optional[str]
    year_of_foundation: Optional[int]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    number_of_employees: Optional[int]
    personal_site: Optional[str]
    phone: Optional[str]
    contact_email: Optional[str]
    social_network_link: Optional[str]
    registered_at: Optional[datetime]


class CompanyRead(schemas.BaseUser):
    id: UUID
    inn: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    company_name: Optional[str]
    description: Optional[str]
    field_of_activity: Optional[str]
    year_of_foundation: Optional[int]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    number_of_employees: Optional[int]
    personal_site: Optional[str]
    phone: Optional[str]
    contact_email: Optional[str]
    social_network_link: Optional[str]
    registered_at: Optional[datetime]
    image_id: Optional[UUID]
    image_url: Optional[str]


class CompanyCreate(schemas.BaseUserCreate):
    inn: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class CompanyUpdate(BaseModel):
    description: Optional[str] = None
    field_of_activity: Optional[str] = None
    year_of_foundation: Optional[int] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    number_of_employees: Optional[int] = None
    # image_id: Optional[UUID] = None
    personal_site: Optional[str] = None
    phone: Optional[str] = None
    social_network_link: Optional[str] = None
    contact_email: Optional[str] = None
    company_name: Optional[str] = None
