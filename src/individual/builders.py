from src.individual.models import Individual, IndividualClt, IndividualSiape, IndividualBeneficio
from .mappers import map_sexo, map_estado_civil, map_situacao_cadastral

def build_entities_from_flat(flat: dict) -> Individual:
    ind = Individual(
        cpf = flat.get("cpf"),
        nome = flat.get("nome"),
        idade = flat.get("idade"),
        veiculo_qtd = flat.get("veiculo_qtd"),
        qtd_empresas_que_e_socio = flat.get("qtd_empresas_que_e_socio"),
        rg = flat.get("rg"),
        nome_mae = flat.get("nome_mae"),
        nome_pai = flat.get("nome_pai"),
        orgao_emissor = flat.get("orgao_emissor")[:3] if flat.get("orgao_emissor") else None,
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

    # CLT
    clt = IndividualClt(
        clt_qtd_pessoas = flat.get("clt_qtd_pessoas"),
        clt_cbo = flat.get("clt_cbo"),
        clt_renda_presumida = flat.get("clt_renda_presumida"),
        clt_renda_presumida_valor = flat.get("clt_renda_presumida_valor"),
    )
    ind.clt = clt

    # SIAPE
    siape = IndividualSiape(
        siape_tipo = flat.get("siape_tipo"),
        siape_margem = flat.get("siape_margem"),
        siape_contrato = flat.get("siape_contrato"),
        siape_matricula = flat.get("siape_matricula"),
        siape_faixa_renda = flat.get("siape_faixa_renda"),
        siape_faixa_renda_valor = flat.get("siape_faixa_renda_valor"),
        siape_valor_total_parcela = flat.get("siape_valor_total_parcela"),
        siape_valor_total_contrato = flat.get("siape_valor_total_contrato"),
    )
    ind.siape = siape

    # Benefício
    benef = IndividualBeneficio(
        beneficio_qtd = flat.get("beneficio_qtd"),
        beneficio_emprestimo = flat.get("beneficio_emprestimo"),
        beneficio_renda = flat.get("beneficio_renda"),
        beneficio_renda_total = flat.get("beneficio_renda_total"),
        beneficio_renda_total_valor = flat.get("beneficio_renda_total_valor"),
    )
    ind.beneficio = benef

    return ind