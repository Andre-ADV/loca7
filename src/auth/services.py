from fastapi import HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from ..users.services import UsersService

from .auth_handler import generate_token, token_response
from .jwt_bearer import JWTBearer
from .schemas import  TokenScheme, UserAuthScheme

user_service = UsersService()

async def get_current_user(token: Annotated[TokenScheme, JWTBearer()]):
    return await user_service.get_user_by_id(token.sub) 

async def authenticate(userAuth: UserAuthScheme, db: AsyncSession):
    user = await user_service.get_user_by_email(userAuth.email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if (user.password == userAuth.senha):
        token = generate_token(user.id_)
        return token_response(token)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

