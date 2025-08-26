from typing import Dict, Any
from decimal import Decimal
from .utils import parse_bool, parse_int_from_any, parse_decimal_currency_br, parse_date_br
# ↑ pode deixar as utils no mesmo arquivo se preferir, ou em utils_parse.py separado

def flatten_infoqualy(resp: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforma o JSON da API Infoqualy em um dicionário pronto para alimentar os models.
    """
    base: Dict[str, Any] = {}

    for bloco in resp.get("RETORNO", []):
        if "id_consulta" in bloco:
            base["id_consulta"] = bloco.get("id_consulta")

        if "CPF" in bloco:
            base.update({
                "cpf": str(bloco.get("CPF") or "").strip() or None,
                "nome": (bloco.get("NOME") or "").strip() or None,
                "idade": parse_int_from_any(bloco.get("idade")),
                "rg": (bloco.get("RG") or "").strip() or None,
                "orgao_emissor": (bloco.get("OrgaoEmissor") or "").strip() or None,
                "escolaridade": (bloco.get("Escolaridade") or "").strip() or None,
                "nome_mae": (bloco.get("NOME_MAE") or "").strip() or None,
                "nome_pai": (bloco.get("NOME_PAI") or "").strip() or None,
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
                "veiculo_qtd": parse_int_from_any(bloco.get("VeiculosQTD")),
                "qtd_empresas_que_e_socio": parse_int_from_any(bloco.get("QtdEmpresasQueEhSocio")),
                # CLT
                "clt_qtd_pessoas": parse_int_from_any(bloco.get("CLT_QtdPessoas")),
                "clt_cbo": (bloco.get("CLT_CBO") or "").strip() or None,
                "clt_renda_presumida": (bloco.get("CLT_RendaPresumida") or "").strip() or None,
                "clt_renda_presumida_valor": parse_decimal_currency_br(bloco.get("CLT_RendaPresumida_vlr")),
                # SIAPE
                "siape_tipo": (bloco.get("Siape_Tipo") or "").strip() or None,
                "siape_margem": (bloco.get("Siape_Margem") or "").strip() or None,
                "siape_contrato": (bloco.get("Siape_Contratos") or "").strip() or None,
                "siape_matricula": (bloco.get("Siape_Matriculas") or "").strip() or None,
                "siape_faixa_renda": parse_decimal_currency_br(bloco.get("Siape_Faixa_Renda")),
                "siape_faixa_renda_valor": parse_decimal_currency_br(bloco.get("Siape_Faixa_Renda_vlr")),
                "siape_valor_total_parcela": parse_decimal_currency_br(bloco.get("Siape_vlt_Tot_Parcelas")),
                "siape_valor_total_contrato": parse_decimal_currency_br(bloco.get("Siape_vlt_Tot_Contratos")),
                # Benefício
                "beneficio_qtd": parse_int_from_any(bloco.get("Beneficio_QtdBeneficios")),
                "beneficio_emprestimo": (bloco.get("Beneficio_FazEmprestimo") or "").strip() or None,
                "beneficio_renda": parse_bool(bloco.get("Beneficio_TemRenda")),
                "beneficio_renda_total": float(Decimal(str(bloco.get("Beneficio_RendaTotal") or "0"))),
                "beneficio_renda_total_valor": parse_decimal_currency_br(bloco.get("Beneficio_RendaTotal_vlr")),
            })
    return base