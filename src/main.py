import logging
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.config import log_config
from src.routers.vacancy import router as vacancy_router
from src.routers.company import router as company_router
from src.routers.photo import router as photo_router
from src.routers.auth import router as auth_router

app = FastAPI(title='Vacancies service')

app.include_router(vacancy_router, tags=['vacancy'])
app.include_router(company_router, tags=['company'])
app.include_router(photo_router, tags=['photo'])
app.include_router(auth_router, tags=['auth'])

# logging.config.dictConfig(log_config)

origins = [
    "http://localhost:8000/",
    "https://front-git-main-olgnites-projects.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True) #, log_config=log_config)
