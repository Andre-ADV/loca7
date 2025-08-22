from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.auth.schemas import AuthLogin

auth_router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@auth_router.get("/")
def authenticate(auth_login: AuthLogin) -> JSONResponse:
    return JSONResponse(
        content = {
            "message": "Trying to authenticate",
        }, status_code = 200
    )

