from typing import Optional, Dict, Any, List
from src.individual.models import (
    Individual, IndividualClt, IndividualSiape, IndividualBeneficio,
    IndividualAddress, IndividualPhone, IndividualEmail
)
from .mappers import map_sexo, map_estado_civil, map_situacao_cadastral

def build_entities_from_flat(flat: Dict[str, Any]) -> Individual:
    ind = Individual(
        cpf = flat.get("cpf"),
        nome = flat.get("nome"),
        idade = flat.get("idade"),
        veiculo_qtd = flat.get("veiculo_qtd"),
        qtd_empresas_que_e_socio = flat.get("qtd_empresas_que_e_socio"),
        rg = flat.get("rg"),
        nome_mae = flat.get("nome_mae"),
        nome_pai = flat.get("nome_pai"),
        orgao_emissor = (flat.get("orgao_emissor")[:3] if flat.get("orgao_emissor") else None),
        escolaridade = flat.get("escolaridade"),
        bcp = flat.get("bcp"),
        pep = flat.get("pep"),
        obito = flat.get("obito"),
        clt_renda = flat.get("clt_renda"),
        tem_siape = flat.get("tem_siape"),
        socio_empresa = flat.get("socio_empresa"),
        veiculo_associado = flat.get("veiculo_associado"),
        auxilio_emergencial = flat.get("auxilio_emergencial"),
        representante_legal = flat.get("representante_legal"),
        auxilio_bolsa_familia = flat.get("auxilio_bolsa_familia"),
        data_obito = flat.get("data_obito"),
        data_nascimento = flat.get("data_nascimento"),
        data_situacao_cadastral = flat.get("data_situacao_cadastral"),
        sexo = map_sexo(flat.get("sexo_raw")),
        estado_civil = map_estado_civil(flat.get("estado_civil_raw")),
        situacao_cadastral = map_situacao_cadastral(flat.get("situacao_cadastral_raw")),
    )

    # --- CLT 1:1 ---
    ind.clt = IndividualClt(
        clt_qtd_pessoas = flat.get("clt_qtd_pessoas"),
        clt_cbo = flat.get("clt_cbo"),
        clt_renda_presumida = flat.get("clt_renda_presumida"),
        clt_renda_presumida_valor = flat.get("clt_renda_presumida_valor"),
    )

    # --- SIAPE 1:1 ---
    ind.siape = IndividualSiape(
        siape_tipo = flat.get("siape_tipo"),
        siape_margem = flat.get("siape_margem"),
        siape_contrato = flat.get("siape_contrato"),
        siape_matricula = flat.get("siape_matricula"),
        siape_faixa_renda = flat.get("siape_faixa_renda"),
        siape_faixa_renda_valor = flat.get("siape_faixa_renda_valor"),
        siape_valor_total_parcela = flat.get("siape_valor_total_parcela"),
        siape_valor_total_contrato = flat.get("siape_valor_total_contrato"),
    )

    # --- Benefício 1:1 ---
    ind.beneficio = IndividualBeneficio(
        beneficio_qtd = flat.get("beneficio_qtd"),
        beneficio_emprestimo = flat.get("beneficio_emprestimo"),
        beneficio_renda = flat.get("beneficio_renda"),
        beneficio_renda_total = flat.get("beneficio_renda_total"),
        beneficio_renda_total_valor = flat.get("beneficio_renda_total_valor"),
    )

    # --- Endereços N:1 ---
    for e in flat.get("enderecos", []) or []:
        ind.enderecos.append(IndividualAddress(
            tipo=e.get("tipo"),
            titulo=e.get("titulo"),
            nome=e.get("nome"),
            numero=e.get("numero"),
            complemento=e.get("complemento"),
            bairro=e.get("bairro"),
            cidade=e.get("cidade"),
            uf=e.get("uf"),
            cep=e.get("cep"),
            endereco=e.get("endereco"),
        ))

    # --- Telefones N:1 ---
    for t in flat.get("telefones", []) or []:
        numero = (t.get("numero") or "").strip()
        if not numero:
            continue
        ind.telefones.append(IndividualPhone(
            tipo=t.get("tipo") or "CELULAR",   # default
            numero=numero,
            ordem=t.get("ordem"),
            whatsapp=t.get("whatsapp"),
            procon=t.get("procon"),
            blocklist=t.get("blocklist"),
            hot=t.get("hot"),
        ))

    # --- Emails N:1 ---
    for em in flat.get("emails", []) or []:
        email = (em.get("email") or "").strip()
        if not email:
            continue
        ind.emails.append(IndividualEmail(
            email=email,
            prioridade=em.get("prioridade"),
        ))

    return ind