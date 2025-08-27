

from datetime import datetime
from decimal import Decimal

from src.database.database import Base
from src.individual.enums import SexoType, EstadoCivilType, SituacaoCadastralType

from sqlalchemy import Float, Integer, String, Boolean, DateTime, Numeric, SmallInteger, func, Enum, text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List, Optional


class Individual(Base):
    __tablename__ = "individual"

    id_:                      Mapped[int]                   = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    idade:                    Mapped[int]                   = mapped_column(Integer, nullable=True)
    veiculo_qtd:              Mapped[int]                   = mapped_column(Integer, nullable=True)
    qtd_empresas_que_e_socio: Mapped[int]                   = mapped_column(Integer, nullable=True)
    rg:                       Mapped[str]                   = mapped_column(String(20), nullable=True, unique=True)
    cpf:                      Mapped[str]                   = mapped_column(String(11), nullable=False, unique=True)
    nome:                     Mapped[str]                   = mapped_column(String(255), nullable=False)
    nome_mae:                 Mapped[str]                   = mapped_column(String(255), nullable=True)
    nome_pai:                 Mapped[str]                   = mapped_column(String(255), nullable=True)
    orgao_emissor:            Mapped[str]                   = mapped_column(String(3), nullable=True)
    escolaridade:             Mapped[str]                   = mapped_column(String(100), nullable=True)
    bcp:                      Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    pep:                      Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    obito:                    Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    clt_renda:                Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    tem_siape:                Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    socio_empresa:            Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    veiculo_associado:        Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    auxilio_emergencial:      Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    representante_legal:      Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    auxilio_bolsa_familia:    Mapped[bool]                  = mapped_column(Boolean, nullable=True)
    data_obito:               Mapped[datetime]              = mapped_column(DateTime, nullable=True)
    data_criacao:             Mapped[datetime]              = mapped_column(DateTime, server_default=func.now())
    data_nascimento:          Mapped[datetime]              = mapped_column(DateTime, nullable=True)
    data_atualizacao:         Mapped[datetime]              = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    data_situacao_cadastral:  Mapped[datetime]              = mapped_column(DateTime, nullable=True)
    sexo:                     Mapped[SexoType]              = mapped_column(Enum(SexoType), nullable=True)
    estado_civil:             Mapped[EstadoCivilType]       = mapped_column(Enum(EstadoCivilType), nullable=True)
    situacao_cadastral:       Mapped[SituacaoCadastralType] = mapped_column(Enum(SituacaoCadastralType), nullable=True)
    clt:                      Mapped["IndividualClt"]       = relationship(back_populates="individual", uselist=False, cascade="all, delete-orphan")
    siape:                    Mapped["IndividualSiape"]     = relationship(back_populates="individual", uselist=False, cascade="all, delete-orphan")
    beneficio:                Mapped["IndividualBeneficio"] = relationship(back_populates="individual", uselist=False, cascade="all, delete-orphan")
    
    enderecos  = relationship("IndividualAddress", back_populates="individual", lazy="selectin", cascade="all, delete-orphan")
    telefones  = relationship("IndividualPhone",   back_populates="individual", lazy="selectin", cascade="all, delete-orphan")
    emails     = relationship("IndividualEmail",   back_populates="individual", lazy="selectin", cascade="all, delete-orphan")
    
class IndividualSiape(Base):
    
    __tablename__ = "individual_siape"
    
    id_:                        Mapped[int]          = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:              Mapped[int]          = mapped_column(ForeignKey("individual.id"), unique=True, nullable=False)
    siape_tipo:                 Mapped[str]          = mapped_column(String(100), nullable=True)
    siape_margem:               Mapped[str]          = mapped_column(String(100), nullable=True)
    siape_contrato:             Mapped[str]          = mapped_column(String(100), nullable=True)
    siape_matricula:            Mapped[str]          = mapped_column(String(100), nullable=True)
    siape_faixa_renda:          Mapped[Decimal]      = mapped_column(Numeric(12, 2), nullable=True)
    siape_faixa_renda_valor:    Mapped[Decimal]      = mapped_column(Numeric(12, 2), nullable=True)
    siape_valor_total_parcela:  Mapped[Decimal]      = mapped_column(Numeric(12, 2), nullable=True)
    siape_valor_total_contrato: Mapped[Decimal]      = mapped_column(Numeric(12, 2), nullable=True)
    individual:                 Mapped["Individual"] = relationship(back_populates="siape", uselist=False)

    
    
class IndividualClt(Base):
    
    __tablename__ = "individual_clt"

    id_:                       Mapped[int]          = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:             Mapped[int]          = mapped_column(ForeignKey("individual.id"), unique=True, nullable=False)
    clt_qtd_pessoas:           Mapped[int]          = mapped_column(Integer, nullable=True)
    clt_cbo:                   Mapped[str]          = mapped_column(String(100), nullable=True)
    clt_renda_presumida:       Mapped[str]          = mapped_column(String(100), nullable=True)
    clt_renda_presumida_valor: Mapped[Decimal]      = mapped_column(Numeric(12, 2), nullable=True)
    individual:                Mapped["Individual"] = relationship(back_populates="clt", uselist=False)


class IndividualBeneficio(Base):
    
    __tablename__ = "individual_beneficio"
    
    id_:                         Mapped[int]          = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:               Mapped[int]          = mapped_column(ForeignKey("individual.id"), unique=True, nullable=False)
    beneficio_qtd:               Mapped[int]          = mapped_column(Integer, nullable=True)
    beneficio_emprestimo:        Mapped[str]          = mapped_column(String(100), nullable=True)
    beneficio_renda:             Mapped[bool]         = mapped_column(Boolean, nullable=True)
    beneficio_renda_total:       Mapped[float]        = mapped_column(Float, nullable=True)
    beneficio_renda_total_valor: Mapped[Decimal]      = mapped_column(Numeric(12, 2), nullable=True)
    individual:                  Mapped["Individual"] = relationship(back_populates="beneficio", uselist=False)
    
    
# -----------------------------------------
# Endereços (mapeia RETORNO[2].ENDERECOS[*])
# -----------------------------------------

class IndividualAddress(Base):
    __tablename__ = "individual_address"

    id_:             Mapped[int]       = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:   Mapped[int]       = mapped_column(ForeignKey("individual.id"), index=True, nullable=False)

    tipo:       Mapped[Optional[str]] = mapped_column(String(20), nullable=True)      # LOGR_TIPO
    titulo:     Mapped[Optional[str]] = mapped_column(String(20), nullable=True)      # LOGR_TITULO
    nome:       Mapped[Optional[str]] = mapped_column(String(120), nullable=True)     # LOGR_NOME
    numero:     Mapped[Optional[str]] = mapped_column(String(20), nullable=True)      # LOGR_NUMERO
    complemento:Mapped[Optional[str]] = mapped_column(String(120), nullable=True)     # LOGR_COMPLEMENTO
    bairro:          Mapped[Optional[str]] = mapped_column(String(120), nullable=True)     # BAIRRO
    cidade:          Mapped[Optional[str]] = mapped_column(String(120), nullable=True)     # CIDADE
    uf:              Mapped[Optional[str]] = mapped_column(String(2), nullable=True)       # UF
    cep:             Mapped[Optional[str]] = mapped_column(String(10), nullable=True)      # CEP (guarde como string)
    endereco: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)   # ENDERECO_ateCompl

    created_at:      Mapped[datetime]  = mapped_column(DateTime, server_default=func.now())
    updated_at:      Mapped[datetime]  = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    individual:      Mapped["Individual"] = relationship(back_populates="enderecos", uselist=False)


# -----------------------------------------
# Telefones (mapeia RETORNO[3].CELULAR[*] e RETORNO[4].TELEFONE_FIXO[*])
# -----------------------------------------

class IndividualPhone(Base):
    __tablename__ = "individual_phone"

    id_:             Mapped[int]       = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:   Mapped[int]       = mapped_column(ForeignKey("individual.id"), index=True, nullable=False)

    tipo:            Mapped[str]       = mapped_column(String(10), nullable=False)         # 'CELULAR' ou 'FIXO'
    numero:          Mapped[str]       = mapped_column(String(20), nullable=False)         # CELULAR / TELEFONE
    ordem:           Mapped[Optional[int]] = mapped_column(Integer, nullable=True)         # OrdemTelefone
    whatsapp:    Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)    # -1/0/1 (mantém tri-estado)
    procon:      Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)    # -1/0/1
    blocklist:   Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)    # -1/0/1
    hot:             Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)    # 0/1

    created_at:      Mapped[datetime]  = mapped_column(DateTime, server_default=func.now())
    updated_at:      Mapped[datetime]  = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    individual:      Mapped["Individual"] = relationship(back_populates="telefones", uselist=False)


# -----------------------------------------
# E-mails (mapeia RETORNO[5].EMAIL[*])
# -----------------------------------------

class IndividualEmail(Base):
    __tablename__ = "individual_email"

    id_:             Mapped[int]       = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    individual_id:   Mapped[int]       = mapped_column(ForeignKey("individual.id"), index=True, nullable=False)

    email:           Mapped[str]       = mapped_column(String(255), nullable=False)
    prioridade:      Mapped[Optional[int]] = mapped_column(Integer, nullable=True)         # PRIORIDADE (se vier)

    created_at:      Mapped[datetime]  = mapped_column(DateTime, server_default=func.now())
    updated_at:      Mapped[datetime]  = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    individual:      Mapped["Individual"] = relationship(back_populates="emails", uselist=False)
