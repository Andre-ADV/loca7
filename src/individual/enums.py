import enum

class SexoType(enum.Enum):
    MASCULINO = 'M'
    FEMININO = 'F'
    
class EstadoCivilType(enum.Enum):
    CASADO = 'CASADO(A)'
    SOLTEIRO = 'SOLTEIRO(A)'
    VIUVO = 'VIUVO(A)'
    DIVORCIADO = 'DIVORCIADO(A)'
    SEPARADO = 'SEPARADO(A)'
    UNIAO = 'UNIÃO ESTÁVEL'
    
class SituacaoCadastralType(enum.Enum):
    REGULAR = 'REGULAR'
    PENDENTE = 'PENDENTE DE REGULARIZAÇÃO'
    SUSPENSA = 'SUSPENSA'
    CANCELADA = 'CANCELADA'
    FALECIDO = 'TITULAR FALECIDO'
    NULA = 'NULA'
    

