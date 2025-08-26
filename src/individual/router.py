from fastapi import APIRouter, Depends

from src.database.database import get_db
from src.individual.models import Individual
from src.individual.services import IndividualService
from src.individual.schemas import IndividualResponse
from src.individual.external_api import ExternalAPI

from sqlalchemy.ext.asyncio import AsyncSession

individual_router = APIRouter(
    tags=['individual'],
    prefix='/individual'
)

individual_service = IndividualService()

@individual_router.get('/', response_model=list[IndividualResponse])
async def get_individual(db: AsyncSession = Depends(get_db)) -> list[Individual]:
    return await individual_service.get_individual(db)

@individual_router.get('/{id_}', response_model=IndividualResponse)
async def get_individual_by_id(id_, db: AsyncSession = Depends(get_db)) -> Individual:
    return await individual_service.get_individual_by_id(id_, db)

@individual_router.get('/cpf/{cpf}', response_model=IndividualResponse)
async def get_individual_by_cpf(cpf, db: AsyncSession = Depends(get_db)) -> Individual:
    return await individual_service.get_individual_by_cpf(cpf, db)
