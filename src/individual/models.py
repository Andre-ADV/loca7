import enum

from datetime import datetime
from decimal import Decimal
from src.db.database import Base
from sqlalchemy import Float, Integer, String, Boolean, DateTime, Numeric, func, Enum, text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

class SexoType(enum.Enum):
    MASCULINO = 'M'
    FEMININO = 'F'
    
class EstadoCivilType(enum.Enum):
    CASADO = 'CASADO(A)'
    SOLTEIRO = 'SOLTEIRO(A)'
    VIUVO = 'VIUVO(A)'
    DIVOCIADO = 'DIVORCIADO(A)'
    SEPARADO = 'SEPARADO(A)'
    UNIAO = 'UNIÃO ESTÁVEL'
    
class SituacaoCadastralType(enum.Enum):
    REGULAR = 'REGULAR'
    PENDENTE = 'PENDENTE DE REGULARIZAÇÃO'
    SUSPENSA = 'SUSPENSA'
    CANCELADA = 'CANCELADA'
    FALECIDO = 'TITULAR FALECIDO'
    NULA = 'NULA'

class Individual(Base):
    __tablename__ = "individual"

    id_: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    rg:  Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    nome:      Mapped[str] = mapped_column(String(255), nullable=False)
    nome_mae:  Mapped[str] = mapped_column(String(255), nullable=True)
    nome_pai:  Mapped[str] = mapped_column(String(255), nullable=True)
    orgao_emissor:   Mapped[str] = mapped_column(String(3), nullable=True)
    escolaridade:    Mapped[str] = mapped_column(String(100), nullable=True)
    data_nascimento: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    idade: Mapped[int] = mapped_column(Integer, nullable=True)
    sexo:  Mapped[SexoType] = mapped_column(Enum(SexoType), nullable=True)
    estado_civil:       Mapped[EstadoCivilType] = mapped_column(Enum(EstadoCivilType), nullable=True)
    situacao_cadastral: Mapped[SituacaoCadastralType] = mapped_column(Enum(SituacaoCadastralType), nullable=True)
    data_situacao_cadastral:  Mapped[datetime] = mapped_column(DateTime, nullable=True)
    socio_empresa:            Mapped[bool] = mapped_column(Boolean, nullable=True)
    qtd_empresas_que_e_socio: Mapped[int] = mapped_column(Integer, nullable=True)
    beneficio:     Mapped["IndividualBeneficio"] = relationship(back_populates="individual", uselist=False, cascade="all, delete-orphan")
    representante_legal:         Mapped[bool] = mapped_column(Boolean, nullable=True)
    tem_siape: Mapped[bool] = mapped_column(Boolean, nullable=True)
    siape:     Mapped["IndividualSiape"] = relationship(back_populates="individual", uselist=False, cascade="all, delete-orphan")
    veiculo_associado: Mapped[bool] = mapped_column(Boolean, nullable=True)
    veiculo_qtd:       Mapped[int] = mapped_column(Integer, nullable=True)
    pep:               Mapped[bool] = mapped_column(Boolean, nullable=True)
    clt_renda:         Mapped[bool] = mapped_column(Boolean, nullable=True)
    clt:               Mapped["IndividualClt"] = relationship(back_populates="individual", uselist=False, cascade="all, delete-orphan")
    auxilio_bolsa_familia: Mapped[bool] = mapped_column(Boolean, nullable=True)
    auxilio_emergencial:   Mapped[bool] = mapped_column(Boolean, nullable=True)
    bcp:        Mapped[bool] = mapped_column(Boolean, nullable=True)
    obito:      Mapped[bool] = mapped_column(Boolean, nullable=True)
    data_obito: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    data_criacao: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    data_atualizacao: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    
class IndividualSiape(Base):
    
    __tablename__ = "individual_siape"
    
    id_:                        Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:              Mapped[int] = mapped_column(ForeignKey("individual.id"), unique=True, nullable=False)
    individual:                 Mapped["Individual"] = relationship(back_populates="siape", uselist=False)
    siape_tipo:                 Mapped[str] = mapped_column(String(100), nullable=True)
    siape_matricula:            Mapped[str] = mapped_column(String(100), nullable=True)
    siape_contrato:             Mapped[str] = mapped_column(String(100), nullable=True)
    siape_valor_total_contrato: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    siape_valor_total_parcela:  Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    siape_faixa_renda:          Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    siape_faixa_renda_valor:    Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    siape_margem:               Mapped[str] = mapped_column(String(100), nullable=True)
    
class IndividualClt(Base):
    
    __tablename__ = "individual_clt"
    
    id_:                       Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:             Mapped[int] = mapped_column(ForeignKey("individual.id"), unique=True, nullable=False)
    individual:                Mapped["Individual"] = relationship(back_populates="clt", uselist=False)
    clt_cbo:                   Mapped[str] = mapped_column(String(100), nullable=True)
    clt_qtd_pessoas:           Mapped[int] = mapped_column(Integer, nullable=True)
    clt_renda_presumida:       Mapped[str] = mapped_column(String(100), nullable=True)
    clt_renda_presumida_valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)

class IndividualBeneficio(Base):
    
    __tablename__ = "individual_beneficio"
    
    id_:                         Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:               Mapped[int] = mapped_column(ForeignKey("individual.id"), unique=True, nullable=False)
    individual:                  Mapped["Individual"] = relationship(back_populates="beneficio", uselist=False)
    beneficio_renda:             Mapped[bool] = mapped_column(Boolean, nullable=True)
    beneficio_qtd:               Mapped[int] = mapped_column(Integer, nullable=True)
    beneficio_renda_total:       Mapped[float] = mapped_column(Float, nullable=True)
    beneficio_renda_total_valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=True)
    beneficio_emprestimo:        Mapped[str] = mapped_column(String(100), nullable=True)