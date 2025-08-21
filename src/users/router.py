from fastapi import APIRouter
from fastapi.responses import JSONResponse

users_router = APIRouter(
    tags=['users'],
    prefix='/users'
)

@users_router.get('/')
def index():
    return JSONResponse(content={"message": "Users route"}, status_code=200)
