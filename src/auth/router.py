from fastapi import APIRouter
from fastapi.responses import JSONResponse

auth_router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@auth_router.get("/login")
def login():
    return JSONResponse(content={"message": "Auth route"}, status_code=200)

