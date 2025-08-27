from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.individual.models import (
    Individual, IndividualClt, IndividualSiape, IndividualBeneficio,
    IndividualAddress, IndividualPhone, IndividualEmail
)
from src.individual.mappers import map_sexo, map_estado_civil, map_situacao_cadastral
from src.individual.infoqualy.parser_infoqualy import flatten_infoqualy
from src.individual.builders import build_entities_from_flat  # se já cria filhos, mantém

async def upsert_individual_from_infoqualy_async(
    session: AsyncSession,
    payload_json: dict,
    *,
    replace_children: bool = True,   # True = limpa e recria; False = mescla (aqui implementado o "limpa e recria")
) -> Individual:
    flat = flatten_infoqualy(payload_json)
    if not flat.get("cpf") or not flat.get("nome"):
        raise ValueError("Resposta Infoqualy sem CPF ou NOME.")

    # carrega com relacionamentos para poder limpar/atualizar
    stmt = (
        select(Individual)
        .where(Individual.cpf == flat["cpf"])
        .options(
            selectinload(Individual.enderecos),
            selectinload(Individual.telefones),
            selectinload(Individual.emails),
            selectinload(Individual.clt),
            selectinload(Individual.siape),
            selectinload(Individual.beneficio),
        )
    )
    result = await session.execute(stmt)
    ind: Optional[Individual] = result.scalar_one_or_none()

    if ind is None:
        # Se seu builder já cria endereços/telefones/emails a partir do flat, ótimo.
        # Senão, criaremos abaixo (limpeza+append).
        ind = build_entities_from_flat(flat)
        session.add(ind)
        await session.flush()  # garante ind.id_
    else:
        # --------- Campos "flat" do Individual ---------
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

        # --------- 1:1 (CLT / SIAPE / Benefício) ---------
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

        # --------- N:1 (Endereços / Telefones / Emails) ---------
        # Estratégia: substituir pelos recebidos (replace_children=True).
        # Se quiser mesclar/deduplicar, posso te enviar uma variante.

        # Endereços
        if "enderecos" in flat and replace_children:
            ind.enderecos.clear()
            for e in (flat.get("enderecos") or []):
                ind.enderecos.append(IndividualAddress(
                    individual_id=ind.id_,
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

        # Telefones
        if "telefones" in flat and replace_children:
            ind.telefones.clear()
            for t in (flat.get("telefones") or []):
                numero = (t.get("numero") or "").strip()
                if not numero:
                    continue
                ind.telefones.append(IndividualPhone(
                    individual_id=ind.id_,
                    tipo=t.get("tipo") or "CELULAR",
                    numero=numero,
                    ordem=t.get("ordem"),
                    whatsapp=t.get("whatsapp"),
                    procon=t.get("procon"),
                    blocklist=t.get("blocklist"),
                    hot=t.get("hot"),
                ))

        # Emails
        if "emails" in flat and replace_children:
            ind.emails.clear()
            for em in (flat.get("emails") or []):
                email = (em.get("email") or "").strip()
                if not email:
                    continue
                ind.emails.append(IndividualEmail(
                    individual_id=ind.id_,
                    email=email,
                    prioridade=em.get("prioridade"),
                ))

    # Persiste
    await session.flush()
    await session.commit()

    # Recarrega com selectinload (evita I/O no response)
    stmt_reload = (
        select(Individual)
        .where(Individual.cpf == flat["cpf"])
        .options(
            selectinload(Individual.enderecos),
            selectinload(Individual.telefones),
            selectinload(Individual.emails),
            selectinload(Individual.clt),
            selectinload(Individual.siape),
            selectinload(Individual.beneficio),
        )
    )
    ind = (await session.execute(stmt_reload)).scalar_one()

    return ind