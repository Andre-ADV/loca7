from src.individual.enums import SexoType, EstadoCivilType, SituacaoCadastralType
from src.individual.schemas import IndividualResponse, EnderecoResponse, TelefoneResponse, EmailResponse
from src.individual.models import Individual
from typing import Optional, Union, Iterable

def map_sexo(v: Optional[str]) -> Optional[SexoType]:
    if not v:
        return None
    s = v.strip().lower()
    if s.startswith("masc"):
        return SexoType.MASCULINO
    if s.startswith("fem"):
        return SexoType.FEMININO
    return None

def map_estado_civil(v: Optional[str]) -> Optional[EstadoCivilType]:
    if not v:
        return None
    s = v.strip().upper()
    # ajuste conforme teus valores de enum
    if "SOLTE" in s:   return EstadoCivilType.SOLTEIRO
    if "CASAD" in s:   return EstadoCivilType.CASADO
    if "SEPARA" in s:  return EstadoCivilType.SEPARADO
    if "DIVORC" in s:  return EstadoCivilType.DIVORCIADO
    if "VIUV" in s or "VIÚV" in s: return EstadoCivilType.VIUVO
    return None

def map_situacao_cadastral(v: Optional[str]) -> Optional[SituacaoCadastralType]:
    if not v:
        return None
    s = v.strip().upper()
    # ajuste conforme teu enum
    if "REGULAR" in s:     return SituacaoCadastralType.REGULAR
    if "PENDENTE" in s:    return SituacaoCadastralType.PENDENTE
    if "CANCEL" in s:      return SituacaoCadastralType.CANCELADA
    if "SUSPEN" in s:      return SituacaoCadastralType.SUSPENSA
    if "NULA" in s:        return SituacaoCadastralType.NULA
    return None


def _map_enderecos(items: Optional[Iterable[dict]]):
    if not items:
        return []
    return [
        EnderecoResponse(
            tipo=i.get("tipo"),
            titulo=i.get("titulo"),
            nome=i.get("nome"),
            numero=i.get("numero"),
            complemento=i.get("complemento"),
            bairro=i.get("bairro"),
            cidade=i.get("cidade"),
            uf=i.get("uf"),
            cep=i.get("cep"),
            endereco=i.get("endereco"),
        )
        for i in items
    ]

def _map_telefones(items: Optional[Iterable[dict]]):
    if not items:
        return []
    return [
        TelefoneResponse(
            tipo=i.get("tipo") or "CELULAR",
            numero=i.get("numero") or "",
            ordem=i.get("ordem"),
            whatsapp=i.get("whatsapp"),
            procon=i.get("procon"),
            blocklist=i.get("blocklist"),
            hot=i.get("hot"),
        )
        for i in items
        if (i.get("numero") or "").strip()
    ]

def _map_emails(items: Optional[Iterable[dict]]):
    if not items:
        return []
    return [
        EmailResponse(
            email=i.get("email") or "",
            prioridade=i.get("prioridade"),
        )
        for i in items
        if (i.get("email") or "").strip()
    ]

def to_response(ind_or_dict: Union[Individual, dict]) -> IndividualResponse:
    """
    Aceita um objeto ORM Individual OU um dicionário já 'flattened'
    (ex.: quando veio direto da Infoqualy e você ainda não persistiu).
    """
    # Caso ORM:
    if isinstance(ind_or_dict, Individual):
        ind = ind_or_dict
        return IndividualResponse(
            cpf=ind.cpf,  # mantenha string
            nome=ind.nome,
            rg=ind.rg,
            sexo=(ind.sexo.name if ind.sexo else None),
            nome_mae=ind.nome_mae,
            nome_pai=ind.nome_pai,
            estado_civil=(ind.estado_civil.name if ind.estado_civil else None),
            escolaridade=ind.escolaridade,
            orgao_emissor=ind.orgao_emissor,
            situacao_cadastral=(ind.situacao_cadastral.name if ind.situacao_cadastral else None),
            idade=ind.idade,
            veiculo_qtd=ind.veiculo_qtd,
            qtd_empresas_que_e_socio=ind.qtd_empresas_que_e_socio,
            pep=ind.pep,
            bcp=ind.bcp,
            obito=ind.obito,
            tem_siape=ind.tem_siape,
            clt_renda=ind.clt_renda,
            socio_empresa=ind.socio_empresa,
            veiculo_associado=ind.veiculo_associado,
            representante_legal=ind.representante_legal,
            auxilio_emergencial=ind.auxilio_emergencial,
            auxilio_bolsa_familia=ind.auxilio_bolsa_familia,
            data_situacao_cadastral=ind.data_situacao_cadastral,
            data_nascimento=ind.data_nascimento,
            data_obito=ind.data_obito,
            enderecos=_map_enderecos([
                {
                    "tipo": e.tipo, "titulo": e.titulo, "nome": e.nome,
                    "numero": e.numero, "complemento": e.complemento,
                    "bairro": e.bairro, "cidade": e.cidade, "uf": e.uf,
                    "cep": e.cep, "endereco": e.endereco
                } for e in (ind.enderecos or [])
            ]),
            telefones=_map_telefones([
                {
                    "tipo": t.tipo, "numero": t.numero, "ordem": t.ordem,
                    "whatsapp": t.whatsapp, "procon": t.procon,
                    "blocklist": t.blocklist, "hot": t.hot
                } for t in (ind.telefones or [])
            ]),
            emails=_map_emails([
                {"email": m.email, "prioridade": m.prioridade}
                for m in (ind.emails or [])
            ]),
        )

    # Caso dict (flatten_infoqualy output)
    d = ind_or_dict
    return IndividualResponse(
        cpf=str(d.get("cpf") or ""),
        nome=d.get("nome") or "",
        rg=d.get("rg"),
        sexo=(d.get("sexo_raw") or None),
        nome_mae=d.get("nome_mae"),
        nome_pai=d.get("nome_pai"),
        estado_civil=(d.get("estado_civil_raw") or None),
        escolaridade=d.get("escolaridade"),
        orgao_emissor=d.get("orgao_emissor"),
        situacao_cadastral=(d.get("situacao_cadastral_raw") or None),
        idade=d.get("idade"),
        veiculo_qtd=d.get("veiculo_qtd"),
        qtd_empresas_que_e_socio=d.get("qtd_empresas_que_e_socio"),
        pep=d.get("pep"),
        bcp=d.get("bcp"),
        obito=d.get("obito"),
        tem_siape=d.get("tem_siape"),
        clt_renda=d.get("clt_renda"),
        socio_empresa=d.get("socio_empresa"),
        veiculo_associado=d.get("veiculo_associado"),
        representante_legal=d.get("representante_legal"),
        auxilio_emergencial=d.get("auxilio_emergencial"),
        auxilio_bolsa_familia=d.get("auxilio_bolsa_familia"),
        data_situacao_cadastral=d.get("data_situacao_cadastral"),
        data_nascimento=d.get("data_nascimento"),
        data_obito=d.get("data_obito"),
        enderecos=_map_enderecos(d.get("enderecos")),
        telefones=_map_telefones(d.get("telefones")),
        emails=_map_emails(d.get("emails")),
    )