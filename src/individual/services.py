from src.utils import check_if_exists
from src.database.crud import CRUD
from src.individual.models import Individual
from src.individual.external_api import ExternalAPI
from src.individual.schemas import IndividualResponse
from src.individual.mappers import to_response



from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

class IndividualService(CRUD[Individual]):

    def __init__(self):
        super().__init__(Individual)

    async def get_individual(self, db: AsyncSession) -> list[Individual]:
        return await self.get_all(db)
    
    async def get_individual_by_id(self, id_: int, db: AsyncSession) -> Individual | None:
        individual = await self.get_by_id(id_, db)
        check_if_exists(individual, "Pessoa fisica não encontrada")
        return individual
    
    async def get_individual_by_cpf(self, cpf: str, db: AsyncSession) -> IndividualResponse:
        stmt = (
            select(Individual)
            .where(Individual.cpf == cpf)
            .options(
                selectinload(Individual.enderecos),
                selectinload(Individual.telefones),
                selectinload(Individual.emails),
                selectinload(Individual.clt),
                selectinload(Individual.siape),
                selectinload(Individual.beneficio),
            )
        )

        result = await db.execute(stmt)
        ind: Individual | None = result.scalar_one_or_none()
        
        if not ind:
            external_api = ExternalAPI()
            ind = await external_api.get_data_individual(cpf, db)
            
            if not ind:
                raise HTTPException(status_code=404, detail="CPF não encontrado")

        return to_response(ind)
