from src.auth.auth import auth_backend, fastapi_users
from src.schemas.company import CompanyRead, CompanyCreate
from fastapi import APIRouter

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(CompanyRead, CompanyCreate),
    prefix="/auth",
    tags=["auth"],
)


