from src.utils import check_if_exists
from src.database.crud import CRUD
from src.individual.models import Individual
from src.individual.external_api import ExternalAPI

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class IndividualService(CRUD[Individual]):

    def __init__(self):
        super().__init__(Individual)

    async def get_individual(self, db: AsyncSession) -> list[Individual]:
        return await self.get_all(db)
    
    async def get_individual_by_id(self, id_: int, db: AsyncSession) -> Individual | None:
        individual = await self.get_by_id(id_, db)
        check_if_exists(individual, "Pessoa fisica não encontrada")
        return individual
    
    async def get_individual_by_cpf(self, cpf: str, db: AsyncSession) -> Individual | None:
        result = await db.execute(select(Individual).where(Individual.cpf == cpf))
        individual = result.scalars().first()
        
        if individual:
            return individual

        external_api = ExternalAPI()
        individual = await external_api.get_data_individual(cpf, db)

        if individual:
            return individual

        check_if_exists(individual, "Pessoa física não encontrada")
