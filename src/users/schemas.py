from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class DocType(Enum):
    CPF = 'CPF'
    CNPJ = 'CNPJ'

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str 
    document: str
    doc_type:  DocType = DocType.CPF

class UpdateUser(BaseModel):
    id_: int
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class ReadUser(BaseModel):
    id_: int

class DeleteUser(BaseModel):
    id_: int

class User(BaseModel):
    id_: int
    name: str
    email: str
    document: str

    class Config:
        from_attributes = True

