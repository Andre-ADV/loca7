from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from ..database.database import get_db
from ..auth.jwt_bearer import JWTBearer

from .services import IndividualService
from .schemas import IndividualResponse
from .models import Individual

individual_router = APIRouter(
    tags=['individual'],
    prefix='/individual',
    dependencies=[Depends(JWTBearer())]
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
