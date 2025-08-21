import enum

from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, func, Enum

class DocType(enum.Enum):
    CPF = 'CPF'
    CNPJ = 'CNPJ'

class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class Users(Base):
    __tablename__ = "users"

    id         = Column(Integer,       primary_key=True, autoincrement=True)
    name       = Column(String(50),    nullable=False)
    email      = Column(String(255),   nullable=False)
    password   = Column(String(255),   nullable=False)
    document   = Column(String(14),    nullable=False)
    doc_type   = Column(Enum(DocType), nullable=False)
    is_active  = Column(Boolean,       nullable=False)
    role       = Column(Enum(Role),    nullable=False, default=Role.USER)
    created_at = Column(DateTime,      nullable=False, server_default=func.now())
    updated_at = Column(DateTime,      nullable=False, server_default=func.now(), onupdate=func.now())

