import enum

from datetime import datetime
from src.db.database import Base
from sqlalchemy import Float, Integer, String, Boolean, DateTime, func, Enum, text
from sqlalchemy.orm import mapped_column, Mapped

class DocType(enum.Enum):
    CPF = 'CPF'
    CNPJ = 'CNPJ'

class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class Users(Base):
    __tablename__ = "users"

    id_:        Mapped[int]      = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    name:       Mapped[str]      = mapped_column(String(50),    nullable=False)
    role:       Mapped[Role]     = mapped_column(Enum(Role),    server_default=text("USER"))
    email:      Mapped[str]      = mapped_column(String(255),   nullable=False, unique=True)
    balance:    Mapped[float]    = mapped_column(Float,         server_default=text("0"))
    password:   Mapped[str]      = mapped_column(String(255),   nullable=False)
    document:   Mapped[str]      = mapped_column(String(14),    nullable=False, unique=True)
    doc_type:   Mapped[DocType]  = mapped_column(Enum(DocType), nullable=False)
    is_active:  Mapped[bool]     = mapped_column(Boolean,       server_default=text("1"))
    created_at: Mapped[datetime] = mapped_column(DateTime,      server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime,      server_default=func.now(), onupdate=func.now())

