from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class IndividualResponse(BaseModel):

    rg: Optional[str]
    sexo: Optional[str]
    nome: str
    nome_mae: Optional[str]
    nome_pai: Optional[str]
    estado_civil: Optional[str]
    escolaridade: Optional[str]
    orgao_emissor: Optional[str]
    situacao_cadastral: Optional[str]

    cpf: int
    idade: Optional[int]
    veiculo_qtd: Optional[int]
    qtd_empresas_que_e_socio: Optional[int]

    pep: Optional[bool]
    bcp: Optional[bool]
    obito: Optional[bool]
    tem_siape: Optional[bool]
    clt_renda: Optional[bool]
    socio_empresa: Optional[bool]
    veiculo_associado: Optional[bool]
    representante_legal: Optional[bool]
    auxilio_emergencial: Optional[bool]
    auxilio_bolsa_familia: Optional[bool]

    data_situacao_cadastral: Optional[datetime]
    data_nascimento: Optional[datetime]
    data_obito: Optional[datetime]
