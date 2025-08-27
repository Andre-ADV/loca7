from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# --- Submodelos ---

class EnderecoResponse(BaseModel):
    tipo: Optional[str] = None
    titulo: Optional[str] = None
    nome: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    endereco: Optional[str] = None


class TelefoneResponse(BaseModel):
    tipo: str                                   # "CELULAR" ou "FIXO"
    numero: str
    ordem: Optional[int] = None
    whatsapp: Optional[int] = None          # -1/0/1 conforme a fonte
    procon: Optional[int] = None
    blocklist: Optional[int] = None
    hot: Optional[int] = None


class EmailResponse(BaseModel):
    email: str
    prioridade: Optional[int] = None


# --- Modelo principal ---

class IndividualResponse(BaseModel):
    cpf: int
    nome: str

    rg: Optional[str] = None
    sexo: Optional[str] = None
    nome_mae: Optional[str] = None
    nome_pai: Optional[str] = None
    estado_civil: Optional[str] = None
    escolaridade: Optional[str] = None
    orgao_emissor: Optional[str] = None
    situacao_cadastral: Optional[str] = None

    idade: Optional[int] = None
    veiculo_qtd: Optional[int] = None
    qtd_empresas_que_e_socio: Optional[int] = None

    pep: Optional[bool] = None
    bcp: Optional[bool] = None
    obito: Optional[bool] = None
    tem_siape: Optional[bool] = None
    clt_renda: Optional[bool] = None
    socio_empresa: Optional[bool] = None
    veiculo_associado: Optional[bool] = None
    representante_legal: Optional[bool] = None
    auxilio_emergencial: Optional[bool] = None
    auxilio_bolsa_familia: Optional[bool] = None

    data_situacao_cadastral: Optional[datetime] = None
    data_nascimento: Optional[datetime] = None
    data_obito: Optional[datetime] = None

    # Novas coleções
    enderecos: List[EnderecoResponse] = Field(default_factory=list)
    telefones: List[TelefoneResponse] = Field(default_factory=list)
    emails: List[EmailResponse] = Field(default_factory=list)