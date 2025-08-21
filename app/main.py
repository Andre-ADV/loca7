from fastapi import FastAPI
from app.db import Base, engine
from app.clientes.routes import router as clientes_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])