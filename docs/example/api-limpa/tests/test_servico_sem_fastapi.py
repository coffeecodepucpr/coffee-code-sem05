"""Testes das regras SEM HTTP e SEM FastAPI: só Python e o núcleo."""
import pytest

from app.dominio.erros import GrupoDuplicadoError, GrupoNaoEncontradoError, MateriaInexistenteError


def test_buscar_grupo_inexistente_levanta_erro_de_dominio(servicos):
    servico_grupos, _ = servicos
    with pytest.raises(GrupoNaoEncontradoError):
        servico_grupos.buscar(99)


def test_criar_gera_identificador_e_data(servicos):
    servico_grupos, _ = servicos
    grupo = servico_grupos.criar("Cálculo II na prática", materia_id=1, max_participantes=5)
    assert grupo.grupo_id == 7
    assert grupo.criado_em is not None


def test_criar_com_materia_inexistente(servicos):
    servico_grupos, _ = servicos
    with pytest.raises(MateriaInexistenteError) as erro:
        servico_grupos.criar("Grupo fantasma", materia_id=99)
    assert erro.value.mensagem == "A matéria 99 não existe"


def test_nome_repetido_na_mesma_materia_e_recusado_sem_diferenciar_maiusculas(servicos):
    servico_grupos, _ = servicos
    with pytest.raises(GrupoDuplicadoError):
        servico_grupos.criar("CÁLCULO PASSO A PASSO", materia_id=1)


def test_mesmo_nome_em_outra_materia_e_aceito(servicos):
    servico_grupos, _ = servicos
    assert servico_grupos.criar("Cálculo passo a passo", materia_id=2).grupo_id == 7


def test_alterar_que_falha_nao_corrompe_o_grupo(servicos):
    servico_grupos, _ = servicos
    servico_grupos.criar("Cálculo II na prática", materia_id=1)
    with pytest.raises(GrupoDuplicadoError):
        servico_grupos.alterar(1, nome_grupo="Cálculo II na prática")
    assert servico_grupos.buscar(1).nome_grupo == "Cálculo passo a passo"


def test_listar_devolve_a_pagina_e_o_total(servicos):
    servico_grupos, _ = servicos
    pagina, total = servico_grupos.listar(limit=2, offset=2)
    assert [g.nome_grupo for g in pagina] == ["Modelagem e SQL", "Processos e memória"]
    assert total == 6
