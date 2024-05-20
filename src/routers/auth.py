from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from src.auth.auth import auth_backend, fastapi_users, current_user
from src.db import get_async_session
from src.models import CustomUser
from src.schemas.company import CompanyRead, CompanyCreate
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi_users.password import PasswordHelper

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


@router.put("/auth/change-password")
async def change_password(
        user: CustomUser = Depends(current_user),
        password: str = Form(...),
        new_password: str = Form(...),
        session: AsyncSession = Depends(get_async_session)
):
    psh = PasswordHelper()
    is_valid, _ = psh.verify_and_update(password, user.hashed_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid current password")

    hashed_password = psh.hash(new_password)
    user.hashed_password = hashed_password
    await session.commit()
    return JSONResponse(status_code=200, content={'message': 'Password changed successfully'})
