from fastapi import HTTPException, Response, status
from src.db.crud import CRUD

from src.users.models import Users
from src.users.schemas import DeleteUser, User

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

class UsersService(CRUD[Users]):

    def __init__(self):
        super().__init__(Users)

    async def get_users(self, db: AsyncSession) -> list[Users]:
        return await self.get_all(db)
    
    async def get_user_by_id(self, id_: int, db: AsyncSession) -> Users | None:
        user = await self.get_by_id(id_, db)
        if not user:
            raise HTTPException(
                status_code = 404,
                detail = "Usuário não encontrado"
            )
        return user
    
    async def get_user_by_email(self, email: str, db: AsyncSession) -> Users | None:
        user = await db.execute(select(Users).where(Users.email == email))
        return user.scalars().first()

    async def get_user_by_document(self, document: str, db: AsyncSession) -> Users | None:
        user = await db.execute(select(Users).where(Users.document == document))
        return user.scalars().first()

    async def create_user(self, user: User, db: AsyncSession) -> Users | None:
        user_by_email = await self.get_user_by_email(user.email, db)
        if user_by_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este email já esta cadastrado")
        
        user_by_cpf = await self.get_user_by_document(user.document, db)
        if user_by_cpf:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este CPF/CNPJ já esta cadastrado")
        
        user.email = user.email.lower()
        user = user.model_dump(exclude_unset=True, exclude_none=True)
        new_user = await self.create(user, db)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ocorreu um erro ao criar usuário"
            )
        
        return new_user
    
    async def update_user(self, user_id: int, user: User, db: AsyncSession) -> Users:
        
        if user.email is not None:
            result = await db.execute(select(Users).where(Users.email == user.email, Users.id_ != user_id))
            if result.scalar() is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este email já esta cadastrado")

        user = user.model_dump(exclude_unset=True, exclude_none=True)
        updated_user = await self.update(user_id, user, db)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        return updated_user
    
    async def delete_user(self, user: DeleteUser, db: AsyncSession) -> Response | None:
        user = await self.get_by_id(user.id_, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        result = await self.delete(user.id_, db)

        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao deletar usuário")
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
