"""Onde as peças são montadas e entregues às rotas (a "raiz de composição").

É o único lugar que escolhe QUAL repositório será usado.
"""
from typing import Annotated, Literal

from fastapi import Depends, Query

from app.aplicacao.servicos import ServicoGrupos, ServicoMaterias
from app.infraestrutura.memoria import novo_repositorio_de_grupos, novo_repositorio_de_materias

_materias = novo_repositorio_de_materias()
_grupos = novo_repositorio_de_grupos()


def obter_servico_materias() -> ServicoMaterias:
    return ServicoMaterias(_materias)


def obter_servico_grupos() -> ServicoGrupos:
    return ServicoGrupos(_grupos, _materias)


def paginacao(
    limit: Annotated[int, Query(ge=1, le=100, description="Quantos itens devolver")] = 10,
    offset: Annotated[int, Query(ge=0, description="Quantos itens pular")] = 0,
) -> dict:
    return {"limit": limit, "offset": offset}


def ordenacao(
    ordenar_por: Annotated[
        Literal["nome_grupo", "max_participantes", "criado_em"], Query(description="Campo de ordenação")
    ] = "nome_grupo",
    ordem: Annotated[Literal["asc", "desc"], Query(description="Sentido da ordenação")] = "asc",
) -> dict:
    return {"ordenar_por": ordenar_por, "ordem": ordem}


ServicoGruposDep = Annotated[ServicoGrupos, Depends(obter_servico_grupos)]
ServicoMateriasDep = Annotated[ServicoMaterias, Depends(obter_servico_materias)]
Paginacao = Annotated[dict, Depends(paginacao)]
Ordenacao = Annotated[dict, Depends(ordenacao)]
