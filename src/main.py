from fastapi import APIRouter, FastAPI

from .users.router import users_router
from .individual.router import individual_router
from .auth.router import auth_router

app = FastAPI()

api = APIRouter(prefix="/api")

api.include_router(users_router)
api.include_router(individual_router)
api.include_router(auth_router)

app.include_router(api)
