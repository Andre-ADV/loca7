from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.jwt_bearer import JWTBearer
from ..database.database import get_db

from .models import Users
from .schemas import CreateUser, DeleteUser, UpdateUser, User
from .services import UsersService

users_router = APIRouter(
    tags=['users'],
    prefix='/users',
    dependencies=[Depends(JWTBearer())]
)

user_service = UsersService()

@users_router.get('/', response_model=list[User])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[Users]:
    return await user_service.get_users(db)

@users_router.get("/{id_}", response_model=User)
async def get_user_by_id(id_: int, db: AsyncSession = Depends(get_db)) -> list[Users]:
    return await user_service.get_user_by_id(id_, db)

@users_router.post('/', response_model=User)
async def create_user(user: CreateUser, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(user, db)

@users_router.patch('/{id_}', response_model=User)
async def update_user(id_: int, user: UpdateUser, db: AsyncSession = Depends(get_db)):
    return await user_service.update_user(id_, user, db)

@users_router.delete('/')
async def delete_user(user: DeleteUser, db: AsyncSession = Depends(get_db)):
    return await user_service.delete_user(user, db)


