from pydantic import BaseModel

class ClienteBase(BaseModel):
    nome: str
    email: str

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id: int

    class Config:
        orm_mode = True