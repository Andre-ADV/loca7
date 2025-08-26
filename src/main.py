from src.users.router import users_router
from src.individual.router import individual_router

from fastapi import APIRouter, FastAPI

app = FastAPI()

api = APIRouter(prefix="/api")

api.include_router(users_router)
api.include_router(individual_router)

app.include_router(api)
