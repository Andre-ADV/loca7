import enum

class DocType(enum.Enum):
    CPF = 'CPF'
    CNPJ = 'CNPJ'

class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"
