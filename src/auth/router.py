from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.database import get_db

from .schemas import TokenResponseScheme, UserAuthScheme
from .services import authenticate

auth_router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)

@auth_router.post("/login", response_model=TokenResponseScheme)
async def login(user: UserAuthScheme, db: AsyncSession = Depends(get_db)):
    return await authenticate(user, db)
