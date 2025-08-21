from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from . import services, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ClienteRead)
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return services.create_cliente(db, cliente)

@router.get("/{cliente_id}", response_model=schemas.ClienteRead)
def ler_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = services.get_cliente(db, cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente

@router.get("/", response_model=list[schemas.ClienteRead])
def listar_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return services.get_clientes(db, skip, limit)