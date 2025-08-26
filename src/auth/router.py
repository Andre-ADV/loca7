from fastapi import APIRouter, Depends

from src.database.database import get_db
from src.auth.schemas import TokenResponseScheme, UserAuthScheme
from src.auth.services import authenticate
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)

@auth_router.post("/login", response_model=TokenResponseScheme)
async def login(user: UserAuthScheme, db: AsyncSession = Depends(get_db)):
    return await authenticate(user, db)
