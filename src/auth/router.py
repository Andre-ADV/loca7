from sqlalchemy.orm import Session
from fastapi import APIRouter
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .config import SECRET_KEY, ALGORITM

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@router.get("/login")
def login():
    return JSONResponse(content={"message": "Auth route"})

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


