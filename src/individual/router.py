from fastapi import APIRouter, Depends

from src.db.database import get_db

from src.individual.models import Individual
from src.individual.services import IndividualService

from sqlalchemy.ext.asyncio import AsyncSession

individual_router = APIRouter(
    tags=['individual'],
    prefix='/individual'
)

individual_service = IndividualService()

@individual_router.get('/', response_model=None)
async def get_individual(db: AsyncSession = Depends(get_db)) -> list[Individual]:
    return await individual_service.get_individual(db)


@individual_router.get('/{id_}', response_model=None)
async def get_individual_by_id(id_, db: AsyncSession = Depends(get_db)) -> list[Individual]:
    return await individual_service.get_individual_by_id(id_, db)


@individual_router.get('/cpf/{cpf}', response_model=None)
async def get_individual_by_cpf(cpf, db: AsyncSession = Depends(get_db)) -> list[Individual]:
    return await individual_service.get_individual_by_cpf(cpf, db)






