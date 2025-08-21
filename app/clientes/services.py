from sqlalchemy.orm import Session
from . import repositorys, schemas

def get_cliente(db: Session, cliente_id: int):
    return repositorys.get_cliente(db, cliente_id)

def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    return repositorys.get_clientes(db, skip, limit)

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    return repositorys.create_cliente(db, cliente.dict())