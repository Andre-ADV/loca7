from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.individual.models import Individual, IndividualClt, IndividualSiape, IndividualBeneficio
from src.individual.mappers import map_sexo, map_estado_civil, map_situacao_cadastral
from src.individual.infoqualy.parser_infoqualy import flatten_infoqualy
from src.individual.builders import build_entities_from_flat

async def upsert_individual_from_infoqualy_async(session: AsyncSession, payload_json: dict) -> Individual:
    flat = flatten_infoqualy(payload_json)
    if not flat.get("cpf") or not flat.get("nome"):
        raise ValueError("Resposta Infoqualy sem CPF ou NOME.")

    result = await session.execute(select(Individual).where(Individual.cpf == flat["cpf"]))
    ind: Optional[Individual] = result.scalar_one_or_none()

    if ind is None:
        ind = build_entities_from_flat(flat)
        session.add(ind)
    else:
        # Atualizações (mesmo conteúdo que você já tem na versão sync)
        ind.nome = flat.get("nome") or ind.nome
        ind.idade = flat.get("idade")
        ind.veiculo_qtd = flat.get("veiculo_qtd")
        ind.qtd_empresas_que_e_socio = flat.get("qtd_empresas_que_e_socio")
        if flat.get("rg"):
            ind.rg = flat["rg"]
        ind.nome_mae = flat.get("nome_mae")
        ind.nome_pai = flat.get("nome_pai")
        ind.orgao_emissor = (flat.get("orgao_emissor")[:3] if flat.get("orgao_emissor") else None)
        ind.escolaridade = flat.get("escolaridade")
        ind.bcp = flat.get("bcp")
        ind.pep = flat.get("pep")
        ind.obito = flat.get("obito")
        ind.clt_renda = flat.get("clt_renda")
        ind.tem_siape = flat.get("tem_siape")
        ind.socio_empresa = flat.get("socio_empresa")
        ind.veiculo_associado = flat.get("veiculo_associado")
        ind.auxilio_emergencial = flat.get("auxilio_emergencial")
        ind.representante_legal = flat.get("representante_legal")
        ind.auxilio_bolsa_familia = flat.get("auxilio_bolsa_familia")
        ind.data_obito = flat.get("data_obito")
        ind.data_nascimento = flat.get("data_nascimento")
        ind.data_situacao_cadastral = flat.get("data_situacao_cadastral")
        ind.sexo = map_sexo(flat.get("sexo_raw"))
        ind.estado_civil = map_estado_civil(flat.get("estado_civil_raw"))
        ind.situacao_cadastral = map_situacao_cadastral(flat.get("situacao_cadastral_raw"))

        if ind.clt is None:
            ind.clt = IndividualClt()
        ind.clt.clt_qtd_pessoas = flat.get("clt_qtd_pessoas")
        ind.clt.clt_cbo = flat.get("clt_cbo")
        ind.clt.clt_renda_presumida = flat.get("clt_renda_presumida")
        ind.clt.clt_renda_presumida_valor = flat.get("clt_renda_presumida_valor")

        if ind.siape is None:
            ind.siape = IndividualSiape()
        ind.siape.siape_tipo = flat.get("siape_tipo")
        ind.siape.siape_margem = flat.get("siape_margem")
        ind.siape.siape_contrato = flat.get("siape_contrato")
        ind.siape.siape_matricula = flat.get("siape_matricula")
        ind.siape.siape_faixa_renda = flat.get("siape_faixa_renda")
        ind.siape.siape_faixa_renda_valor = flat.get("siape_faixa_renda_valor")
        ind.siape.siape_valor_total_parcela = flat.get("siape_valor_total_parcela")
        ind.siape.siape_valor_total_contrato = flat.get("siape_valor_total_contrato")

        if ind.beneficio is None:
            ind.beneficio = IndividualBeneficio()
        ind.beneficio.beneficio_qtd = flat.get("beneficio_qtd")
        ind.beneficio.beneficio_emprestimo = flat.get("beneficio_emprestimo")
        ind.beneficio.beneficio_renda = flat.get("beneficio_renda")
        ind.beneficio.beneficio_renda_total = flat.get("beneficio_renda_total")
        ind.beneficio.beneficio_renda_total_valor = flat.get("beneficio_renda_total_valor")

    await session.commit()
    await session.refresh(ind)
    return ind