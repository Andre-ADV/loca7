from fastapi import HTTPException, Response, status
from src.db.crud import CRUD

from src.individual.models import Individual

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

class IndividualService(CRUD[Individual]):

    def __init__(self):
        super().__init__(Individual)

    async def get_individual(self, db: AsyncSession) -> list[Individual]:
        return await self.get_all(db)
    
    async def get_individual_by_id(self, id_: int, db: AsyncSession) -> Individual | None:
        individual = await self.get_by_id(id_, db)
        if not individual:
            raise HTTPException(
                status_code = 404,
                detail = "Pessoa física não encontrada."
            )
        return individual
    
    async def get_individual_by_cpf(self, cpf: str, db: AsyncSession) -> Individual | None:
        individual = await db.execute(select(Individual).where(Individual.cpf == cpf))
        return individual.scalars().first()
