from typing import Optional, TypeVar, Generic, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")

class CRUD(Generic[Model]):

    def __init__(self, model: Type[Model]) -> None:
        self.model = model

    async def get_all(self, db: AsyncSession) -> list[Model]:
        result = await db.execute(select(self.model))
        return result.scalars().all()
    
    async def get_by_id(self, id: int, db: AsyncSession) -> Optional[Model]:
        return await db.get(self.model, id)
    
    async def create(self, data: dict, db: AsyncSession) -> Model | None:
        try:
            new_obj = self.model(**data)
            db.add(new_obj)
            await db.commit()
            await db.refresh(new_obj)
            return new_obj
        except Exception as e:
            await db.rollback()
            print("Ocorreu um erro ao criar usuário:", e)
            return None
    
    async def update(self, obj_id: int,  data: dict, db: AsyncSession) -> Optional[Model]:
        obj = await db.get(self.model, obj_id)
        if not obj:
            return None
        for k, v in data.items():
            setattr(obj, k, v)
        
        try:
            await db.commit()
            await db.refresh(obj)
            return obj
        except Exception as e:
            await db.rollback()
            print("Ocorreu um erro ao atualizar usuário:", e)

    async def delete(self, obj_id: int, db: AsyncSession) -> bool | None:
        obj = await db.get(self.model, obj_id)
        if not obj:
            return False
        
        try:
            await db.delete(obj)
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            print("Ocorreu um erro ao deletar usuário:", e)
            return None

