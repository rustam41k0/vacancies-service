import uuid
from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, UUID, String, ForeignKey, Integer, Enum as EnumType, TIMESTAMP, Boolean
from src.custom_types import EmploymentEnum, ExperienceEnum
from src.db import Base


class Vacancy(Base):
    __tablename__ = 'vacancy'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    salary = Column(Integer, nullable=False)
    description = Column(String(5000), nullable=False)
    city = Column(String(255), nullable=False)
    employment = Column(EnumType(EmploymentEnum))
    experience = Column(EnumType(ExperienceEnum))
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id', ondelete='CASCADE'), nullable=False)


class Company(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'company'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inn = Column(String(64), unique=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    company_name = Column(String(255), nullable=True)
    description = Column(String(5000), nullable=True)
    field_of_activity = Column(String(512), nullable=True)
    year_of_foundation = Column(Integer, nullable=True)
    city = Column(String(255), nullable=True)
    street = Column(String(255), nullable=True)
    house = Column(String(255), nullable=True)
    number_of_employees = Column(Integer, nullable=True)
    personal_site = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    social_network_link = Column(String(255), nullable=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)


class Image(Base):
    __tablename__ = 'image'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.id', ondelete='CASCADE'), nullable=True)


class CustomUser(Company):
    pass

