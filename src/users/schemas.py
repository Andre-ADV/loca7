from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class DocType(Enum):
    CPF = 'CPF'
    CNPJ = 'CNPJ'

class User(BaseModel):
    id_: int
    name: str
    email: EmailStr
    document: str

    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str 
    document: str
    doc_type: DocType

    class Config:
        use_enum_values = True

class UpdateUser(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class DeleteUser(BaseModel):
    id_: int


