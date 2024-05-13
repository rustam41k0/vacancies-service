import uvicorn
from fastapi import FastAPI
from src.routers.vacancy import router as vacancy_router
from src.routers.company import router as company_router
from src.routers.photo import router as photo_router
from src.routers.auth import router as auth_router

app = FastAPI(title='Vacancies service')
app.include_router(vacancy_router, tags=['vacancy'])
app.include_router(company_router, tags=['company'])
app.include_router(photo_router, tags=['photo'])
app.include_router(auth_router, tags=['auth'])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
