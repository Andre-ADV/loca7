from sqlalchemy.orm import Session
from . import models, schemas

def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente