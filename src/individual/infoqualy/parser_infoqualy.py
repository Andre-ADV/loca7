from typing import Dict, Any
from decimal import Decimal
from ..utils import parse_bool, parse_int_from_any, parse_decimal_currency_br, parse_date_br
import re
from decimal import Decimal, InvalidOperation
from typing import Optional, List

def _norm_str(v):
    return (v or "").strip() or None

def _as_int(v):
    try:
        return int(str(v).strip().split()[0])
    except Exception:
        return None


def parse_decimal_currency_br(v) -> Optional[Decimal]:
    """
    Converte strings como 'R$ 2.748,00', '2.748,00', '2748,00', '0', '' em Decimal.
    Retorna None se não der pra converter.
    """
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    # Remove tudo que não é dígito, ponto, vírgula, sinal
    s = re.sub(r'[^0-9,.\-+]', '', s)
    # Remove separador de milhar ponto e troca vírgula por ponto (padrão BR)
    s = s.replace('.', '').replace(',', '.')
    try:
        return Decimal(s)
    except InvalidOperation:
        return None

def to_float_or_none(d: Optional[Decimal]) -> Optional[float]:
    return float(d) if d is not None else None
   
def flatten_infoqualy(resp: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforma o JSON da Infoqualy em um dicionário com:
      - campos "flat" para Individual/CLT/SIAPE/Benefício
      - listas: enderecos[], telefones[], emails[]
    """
    base: Dict[str, Any] = {}
    enderecos: List[Dict[str, Any]] = []
    telefones: List[Dict[str, Any]] = []
    emails: List[Dict[str, Any]] = []

    for bloco in resp.get("RETORNO", []):
        # 1) bloco de id_consulta
        if "id_consulta" in bloco:
            base["id_consulta"] = bloco.get("id_consulta")

        # 2) bloco de dados principais
        if "CPF" in bloco:
            base.update({
                "cpf": _norm_str(bloco.get("CPF")),
                "nome": _norm_str(bloco.get("NOME")),
                "idade": _as_int(bloco.get("idade")),
                "rg": _norm_str(bloco.get("RG")),
                "orgao_emissor": _norm_str(bloco.get("OrgaoEmissor")),
                "escolaridade": _norm_str(bloco.get("Escolaridade")),
                "nome_mae": _norm_str(bloco.get("NOME_MAE")),
                "nome_pai": _norm_str(bloco.get("NOME_PAI")),
                "sexo_raw": bloco.get("SEXO"),
                "estado_civil_raw": bloco.get("ESTADO_CIVIL"),
                "situacao_cadastral_raw": bloco.get("SITUACAO_CADASTRAL_RF"),
                "data_situacao_cadastral": parse_date_br(bloco.get("DATA_SITUACAO_CADASTRAL_RF")),
                "data_nascimento": parse_date_br(bloco.get("DataNasc")),
                "bcp": parse_bool(bloco.get("BPC")),
                "pep": parse_bool(bloco.get("PEP")),
                "obito": parse_bool(bloco.get("Obito")),
                "data_obito": parse_date_br(bloco.get("DataObito")),
                "clt_renda": parse_bool(bloco.get("CLT_Renda")),
                "tem_siape": parse_bool(bloco.get("Siape")),
                "socio_empresa": parse_bool(bloco.get("SocioEmpresa")),
                "veiculo_associado": parse_bool(bloco.get("VeiculosAssociados")),
                "auxilio_emergencial": parse_bool(bloco.get("AuxEmergencial")),
                "representante_legal": parse_bool(bloco.get("RepresentanteLegal")),
                "auxilio_bolsa_familia": parse_bool(bloco.get("AuxilioBrasil_BolsaFamilia")),
                "veiculo_qtd": _as_int(bloco.get("VeiculosQTD")),
                "qtd_empresas_que_e_socio": _as_int(bloco.get("QtdEmpresasQueEhSocio")),
                # CLT
                "clt_qtd_pessoas": _as_int(bloco.get("CLT_QtdPessoas")),
                "clt_cbo": _norm_str(bloco.get("CLT_CBO")),
                "clt_renda_presumida": _norm_str(bloco.get("CLT_RendaPresumida")),
                "clt_renda_presumida_valor": parse_decimal_currency_br(bloco.get("CLT_RendaPresumida_vlr")),
                # SIAPE
                "siape_tipo": _norm_str(bloco.get("Siape_Tipo")),
                "siape_margem": _norm_str(bloco.get("Siape_Margem")),
                "siape_contrato": _norm_str(bloco.get("Siape_Contratos")),
                "siape_matricula": _norm_str(bloco.get("Siape_Matriculas")),
                "siape_faixa_renda": parse_decimal_currency_br(bloco.get("Siape_Faixa_Renda")),
                "siape_faixa_renda_valor": parse_decimal_currency_br(bloco.get("Siape_Faixa_Renda_vlr")),
                "siape_valor_total_parcela": parse_decimal_currency_br(bloco.get("Siape_vlt_Tot_Parcelas")),
                "siape_valor_total_contrato": parse_decimal_currency_br(bloco.get("Siape_vlt_Tot_Contratos")),
                # Benefício
                "beneficio_qtd": _as_int(bloco.get("Beneficio_QtdBeneficios")),
                "beneficio_emprestimo": _norm_str(bloco.get("Beneficio_FazEmprestimo")),
                "beneficio_renda": parse_bool(bloco.get("Beneficio_TemRenda")),
                "beneficio_renda_total": to_float_or_none(parse_decimal_currency_br(bloco.get("Beneficio_RendaTotal"))),
                "beneficio_renda_total_valor": parse_decimal_currency_br(bloco.get("Beneficio_RendaTotal_vlr")),
            })

        # 3) bloco de endereços
        if "ENDERECOS" in bloco and isinstance(bloco["ENDERECOS"], list):
            for e in bloco["ENDERECOS"]:
                enderecos.append({
                    "tipo": _norm_str(e.get("LOGR_TIPO")),
                    "titulo": _norm_str(e.get("LOGR_TITULO")),
                    "nome": _norm_str(e.get("LOGR_NOME")),
                    "numero": _norm_str(e.get("LOGR_NUMERO")),
                    "complemento": _norm_str(e.get("LOGR_COMPLEMENTO")),
                    "bairro": _norm_str(e.get("BAIRRO")),
                    "cidade": _norm_str(e.get("CIDADE")),
                    "uf": _norm_str(e.get("UF")),
                    "cep": _norm_str(e.get("CEP")),
                    "endereco": _norm_str(e.get("ENDERECO_ateCompl")),
                })

        # 4) bloco de celulares
        if "CELULAR" in bloco and isinstance(bloco["CELULAR"], list):
            for c in bloco["CELULAR"]:
                telefones.append({
                    "tipo": "CELULAR",
                    "numero": _norm_str(c.get("CELULAR")),
                    "ordem": _as_int(c.get("OrdemTelefone")),
                    "whatsapp": _as_int(c.get("flg_WhatsAPP")),
                    "procon": _as_int(c.get("flg_Procon")),
                    "blocklist": _as_int(c.get("flg_BlockList")),
                    "hot": _as_int(c.get("HOT")),
                })

        # 5) bloco de telefone fixo
        if "TELEFONE_FIXO" in bloco and isinstance(bloco["TELEFONE_FIXO"], list):
            for t in bloco["TELEFONE_FIXO"]:
                telefones.append({
                    "tipo": "FIXO",
                    "numero": _norm_str(t.get("TELEFONE")),
                    "ordem": _as_int(t.get("OrdemTelefone")),
                    "whatsapp": _as_int(t.get("flg_WhatsAPP")),
                    "procon": _as_int(t.get("flg_Procon")),
                    "blocklist": _as_int(t.get("flg_BlockList")),
                    "hot": _as_int(t.get("HOT")),
                })

        # 6) bloco de e-mails
        if "EMAIL" in bloco and isinstance(bloco["EMAIL"], list):
            for em in bloco["EMAIL"]:
                emails.append({
                    "email": _norm_str(em.get("EMAIL")),
                    # algumas fontes trazem PRIORIDADE; se não vier, deixa None
                    "prioridade": _as_int(em.get("PRIORIDADE")),
                })

    base["enderecos"] = enderecos
    base["telefones"] = telefones
    base["emails"] = emails
    return base